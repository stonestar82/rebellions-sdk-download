
#!/bin/bash

# sdk_init.sh - 리벨리온 SDK 초기화 스크립트
# Python 가상환경을 생성하고 필요한 패키지를 설치합니다.

# 설정 변수
DEFAULT_PATH="/workspace/rebellions-sdk-download"
PYTHON_VERSIONS=("3.9" "3.10" "3.11")

echo "리벨리온 SDK 초기화를 시작합니다..."

# Python 버전별로 가상환경 생성
for python_version in "${PYTHON_VERSIONS[@]}"; do
    echo "Python ${python_version} 가상환경을 생성합니다..."
    
    # 폴더 확인
    if [ -d "${DEFAULT_PATH}/venv_${python_version}" ]; then
        echo "venv_${python_version} already exists"
        continue
    fi
    
    echo "Python ${python_version} 가상환경을 생성 중..."
    
    # 가상환경 생성
    python${python_version} -m venv "${DEFAULT_PATH}/venv_${python_version}"
    
    if [ $? -eq 0 ]; then
        echo "가상환경 생성 완료: venv_${python_version}"
        
        # 가상환경 활성화
        source "${DEFAULT_PATH}/venv_${python_version}/bin/activate"
        
        # pip 업그레이드
        pip install --upgrade pip
        
        # requirements.txt가 존재하는 경우 설치
        if [ -f "req.txt" ]; then
            echo "req.txt에서 패키지를 설치합니다..."
            pip install -r req.txt
        else
            echo "req.txt 파일을 찾을 수 없습니다. 기본 패키지만 설치합니다..."
            pip install requests beautifulsoup4
        fi
        
        # 가상환경 비활성화
        deactivate
        
        echo "Python ${python_version} 가상환경 설정이 완료되었습니다."
    else
        echo "오류: Python ${python_version} 가상환경 생성에 실패했습니다."
        rm -rf "${DEFAULT_PATH}/venv_${python_version}"
        exit 1
    fi
done

echo "모든 Python 가상환경 생성이 완료되었습니다."
echo "생성된 가상환경:"
for python_version in "${PYTHON_VERSIONS[@]}"; do
    if [ -d "${DEFAULT_PATH}/venv_${python_version}" ]; then
        echo "  - venv_${python_version}"
    fi
done