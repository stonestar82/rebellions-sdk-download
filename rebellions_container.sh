#!/bin/bash

NFS_SDK_PATH="/srv/nfs/share/SDK"

# Dockerfile 존재 여부 확인
if [ ! -f "$NFS_SDK_PATH/Dockerfile" ]; then
    echo "Error: $NFS_SDK_PATH/Dockerfile 파일이 존재하지 않습니다."
    exit 1
fi

echo "Dockerfile이 존재합니다. 작업을 시작합니다..."

TAG=$(docker images --format '{{.Repository}} {{.Tag}}' | awk '$1=="ubuntu-rebellions"{print $2}')
echo $TAG


# 기존 ubuntu-rebellions 이미지 삭제
echo "기존 ubuntu-rebellions 이미지를 삭제합니다..."
docker rmi ubuntu-rebellions:$TAG 2>/dev/null || echo "삭제할 ubuntu-rebellions 이미지가 없습니다."

# release_info.txt 파일에서 release 값 추출
if [ ! -f "$NFS_SDK_PATH/release_info.txt" ]; then
    echo "Error: $NFS_SDK_PATH/release_info.txt 파일이 존재하지 않습니다."
    exit 1
fi

echo "release_info.txt에서 release 값을 추출합니다..."
RELEASE_VALUE=$(head -n 1 $NFS_SDK_PATH/release_info.txt | grep -o 'release=[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | cut -d'=' -f2)

if [ -z "$RELEASE_VALUE" ]; then
    echo "Error: release 값을 추출할 수 없습니다."
    exit 1
fi

echo "추출된 release 값: $RELEASE_VALUE"

# Docker 이미지 빌드
echo "Docker 이미지를 빌드합니다..."
docker build --no-cache -t ubuntu-rebellions:$RELEASE_VALUE $NFS_SDK_PATH/

if [ $? -ne 0 ]; then
    echo "Error: Docker 이미지 빌드에 실패했습니다."
    exit 1
fi

echo "Docker 이미지 빌드가 완료되었습니다."

# Docker 이미지를 tar 파일로 저장
echo "Docker 이미지를 tar 파일로 저장합니다..."
docker save -o ubuntu-rebellions.$RELEASE_VALUE.tar ubuntu-rebellions:$RELEASE_VALUE

if [ $? -ne 0 ]; then
    echo "Error: Docker 이미지 저장에 실패했습니다."
    exit 1
fi

echo "Docker 이미지가 ubuntu-rebellions.$RELEASE_VALUE.tar 파일로 저장되었습니다."


# docker_load.sh 스크립트 생성
echo "docker_load.sh 스크립트를 생성합니다..."
cat > docker_load.sh << EOF
#!/bin/bash

docker load -i ubuntu-rebellions.$RELEASE_VALUE.tar
EOF

chmod +x docker_load.sh
echo "docker_load.sh 스크립트가 생성되었습니다."

# docker_run.sh 스크립트 생성
echo "docker_run.sh 스크립트를 생성합니다..."
cat > docker_run.sh << EOF
#!/bin/bash

# Parameter validation
if [ \$# -ne 1 ]; then
	echo "Usage: \$0 <device count (1-16)>"
	exit 1
fi

DEVICE_COUNT=\$1

# Parameter range validation (1-16)
if [ \$DEVICE_COUNT -lt 1 ] || [ \$DEVICE_COUNT -gt 16 ]; then
	echo "Error: Device count must be between 1-16."
	exit 1
fi

# Generate device options
DEVICE_OPTIONS=""
for i in \$(seq 0 \$((DEVICE_COUNT-1))); do
	DEVICE_OPTIONS="\$DEVICE_OPTIONS --device /dev/rbln\$i"
done

docker run \\
			--device /dev/rsd0 \\
			\$DEVICE_OPTIONS \\
			--volume /usr/local/bin/rbln-stat:/usr/local/bin/rbln-stat \\
			--volume /root/.cache:/root/.cache \\
			-ti ubuntu-rebellions:$RELEASE_VALUE
EOF

chmod +x docker_run.sh
echo "docker_run.sh 스크립트가 생성되었습니다."

# ubuntu-rebellions.$RELEASE_VALUE.tar와 docker_run.sh를 하나의 파일로 압축
echo "Docker 이미지 tar 파일과 docker_run.sh를 하나의 파일로 압축합니다..."
tar -czf ubuntu-rebellions.$RELEASE_VALUE.tar.gz ubuntu-rebellions.$RELEASE_VALUE.tar docker_run.sh docker_load.sh

if [ $? -ne 0 ]; then
	echo "Error: 파일 압축에 실패했습니다."
	exit 1
fi

echo "ubuntu-rebellions.$RELEASE_VALUE.tar.gz 파일이 생성되었습니다."

# 개별 파일들 삭제 (선택사항)
echo "개별 파일들을 삭제합니다..."
rm ubuntu-rebellions.$RELEASE_VALUE.tar docker_run.sh docker_load.sh

# Dockerfile 삭제
echo "Dockerfile을 삭제합니다..."
rm $NFS_SDK_PATH/Dockerfile
rm $NFS_SDK_PATH/resnet_test.sh

if [ $? -ne 0 ]; then
	echo "Error: Dockerfile 삭제에 실패했습니다."
	exit 1
fi


## 기존 폴더에 파일 삭제
rm -rf /srv/nfs/share/docker/*

## 최종파일 이동
mv ubuntu-rebellions.$RELEASE_VALUE.tar.gz /srv/nfs/share/docker/

echo "모든 작업이 완료되었습니다!"
echo "- 빌드된 이미지: ubuntu-rebellions:$RELEASE_VALUE"
echo "- 최종 압축 파일: ubuntu-rebellions.$RELEASE_VALUE.tar.gz"
echo "  (포함: ubuntu-rebellions.$RELEASE_VALUE.tar + docker_run.sh + docker_load.sh)"
