from sdk_common import DEFAULT_PATH, NFS_SDK_PATH, ERROR_FILE_NAME, REBELLIONS_ID, REBELLIONS_PW, PYTHON_VERSIONS
from jinja2 import Template
import os

## 파이썬 버전별로 가상환경 생성


template = """
#!/bin/bash

# sdk_init.sh - 리벨리온 SDK 초기화 스크립트
# Python 가상환경을 생성하고 필요한 패키지를 설치합니다.

# 설정 변수
DEFAULT_PATH="{{ DEFAULT_PATH }}"
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
"""

t = Template(template)

with open("sdk_init.sh", "w", encoding="utf-8") as f:
	f.write(t.render(DEFAULT_PATH=DEFAULT_PATH, PYTHON_VERSIONS=PYTHON_VERSIONS))


# Windows에서는 chmod가 필요하지 않음
if os.name != 'nt':  # Unix/Linux/Mac
    os.system("chmod +x sdk_init.sh")



template = """
#!/bin/bash

# sdk_download.sh - Rebellions SDK Download Script
# Downloads and packages Compiler, Optimum, and VLLM SDKs

# Configuration variables
DEFAULT_PATH="{{ DEFAULT_PATH }}"
NFS_SDK_PATH="{{ NFS_SDK_PATH }}"   
REBELLIONS_ID="{{ REBELLIONS_ID }}"
REBELLIONS_PW="{{ REBELLIONS_PW }}"
PYTHON_VERSIONS=("3.9" "3.10" "3.11")

# Check external parameters (3 required)
if [ $# -ne 3 ]; then
	echo "============================================================================"
	echo "read release_info.txt"
	compiler_version=$(grep "compiler_version" ${NFS_SDK_PATH}/release_info.txt | cut -d'=' -f2)
	optimum_version=$(grep "optimum_version" ${NFS_SDK_PATH}/release_info.txt | cut -d'=' -f2)
	vllm_version=$(grep "vllm_version" ${NFS_SDK_PATH}/release_info.txt | cut -d'=' -f2)
	echo "compiler version: ${compiler_version}"
	echo "optimum version: ${optimum_version}"
	echo "vllm version: ${vllm_version}"
	echo "============================================================================"
	echo ""
	sleep 5
	echo "################################################################"
	echo "# if you want to download again, please try again"
	echo "# Usage: $0 <compiler_version> <optimum_version> <vllm_version>"
	echo "# Example: $0 0.8.2 0.8.2 0.8.2"
	echo "################################################################"
	echo ""
	sleep 5
else
	compiler_version="$1"
	optimum_version="$2"
	vllm_version="$3"
fi

for python_version in "${PYTHON_VERSIONS[@]}"; do
    echo "============================================================================"
    echo "Starting Python ${python_version} virtual environment processing"
    echo "============================================================================"
    
    # Check virtual environment path
    venv_path="${DEFAULT_PATH}/venv_${python_version}"
    
    if [ ! -d "$venv_path" ]; then
        echo "Warning: Virtual environment does not exist: $venv_path"
        echo "Skipping to next Python version."
        continue
    fi
    
    # Activate virtual environment
    if [ -f "${venv_path}/bin/activate" ]; then
        echo "Activating virtual environment: $venv_path"
        source "${venv_path}/bin/activate"
        
        # Verify virtual environment activation
        if [ -n "$VIRTUAL_ENV" ]; then
            echo "Virtual environment activated successfully: $VIRTUAL_ENV"
            echo "Python version: $(python --version)"
            echo "Pip version: $(pip --version)"
        else
            echo "Error: Failed to activate virtual environment."
            continue
        fi
    else
        echo "Error: Virtual environment activation script not found: ${venv_path}/bin/activate"
        continue
    fi

    # Main script start
    echo "============================================================================"
    echo "rebellion studio sdk downloader python ${python_version}"
    echo "============================================================================"

	
	

	echo "compiler_version: $compiler_version"
	echo "optimum_version: $optimum_version"
	echo "vllm_version: $vllm_version"

	sleep 1

	final_tar_name="rebellions_sdk_python-${python_version}_compiler-${compiler_version}_optimum-${optimum_version}_vllm-${vllm_version}.tar"

	echo "final_tar_name: ${final_tar_name}"

	# Check if file already exists
	if [ -f "${NFS_SDK_PATH}/${final_tar_name}" ]; then
		echo "File already exists: ${NFS_SDK_PATH}/${final_tar_name}"
		echo "Skipping to next Python version."
		continue
	fi


	# Create pip directory
	mkdir -p "${NFS_SDK_PATH}/pip"

	# 1. Compiler SDK download
	echo "============================================================================"
	echo "compiler sdk download start : v$compiler_version"
	echo "============================================================================"

	cmd="pip download --extra-index-url https://${REBELLIONS_ID}:${REBELLIONS_PW}@pypi.rbln.ai/simple rebel-compiler==${compiler_version} -d ${NFS_SDK_PATH}/pip"
	# echo "Executing command: $cmd"

	if eval "$cmd"; then
			echo "Compiler SDK download completed"
	else
			echo "Compiler SDK download failed"
			exit 1
	fi

	sleep 1

	# Find Compiler SDK file
	compiler_sdk_files=($(find "${NFS_SDK_PATH}/pip" -name "rebel_compiler-${compiler_version}-*.whl" -type f))

	if [ ${#compiler_sdk_files[@]} -eq 0 ]; then
			echo "compiler sdk file not found"
			exit 1
	fi

	compiler_sdk_file="${compiler_sdk_files[0]}"
	echo "compiler sdk file found : $compiler_sdk_file"

	# 2. Optimum SDK download
	echo "============================================================================"
	echo "optimum sdk download start : v$optimum_version"
	echo "============================================================================"

	cmd="pip download --extra-index-url https://${REBELLIONS_ID}:${REBELLIONS_PW}@pypi.rbln.ai/simple optimum-rbln==${optimum_version} -d ${NFS_SDK_PATH}/pip"
	# echo "Executing command: $cmd"

	if eval "$cmd"; then
			echo "Optimum SDK download completed"
	else
			echo "Optimum SDK download failed"
			exit 1
	fi

	sleep 1

	# Find Optimum SDK file
	optimum_sdk_files=($(find "${NFS_SDK_PATH}/pip" -name "optimum_rbln-${optimum_version}-*.whl" -type f))

	if [ ${#optimum_sdk_files[@]} -eq 0 ]; then
			echo "optimum sdk file not found"
			exit 1
	fi

	optimum_sdk_file="${optimum_sdk_files[0]}"
	echo "optimum sdk file found : $optimum_sdk_file"

	# 3. VLLM SDK download
	echo "============================================================================"
	echo "vllm sdk download start : v$vllm_version"
	echo "============================================================================"

	cmd="pip download --extra-index-url https://${REBELLIONS_ID}:${REBELLIONS_PW}@pypi.rbln.ai/simple vllm-rbln==${vllm_version} -d ${NFS_SDK_PATH}/pip"
	# echo "Executing command: $cmd"

	if eval "$cmd"; then
			echo "VLLM SDK download completed"
	else
			echo "VLLM SDK download failed"
			exit 1
	fi

	sleep 1

	# Find VLLM SDK file
	vllm_sdk_files=($(find "${NFS_SDK_PATH}/pip" -name "vllm_rbln-${vllm_version}-*.whl" -type f))

	if [ ${#vllm_sdk_files[@]} -eq 0 ]; then
			echo "vllm sdk file not found"
			exit 1
	fi

	vllm_sdk_file="${vllm_sdk_files[0]}"
	echo "vllm sdk file found : $vllm_sdk_file"

	# 4. Create tar file
	echo "============================================================================"
	echo "tar file create start"
	echo "============================================================================"

	cmd="tar -cf ${NFS_SDK_PATH}/pip.tar -C ${NFS_SDK_PATH}/pip ."
	echo "Executing command: $cmd"

	if eval "$cmd"; then
			echo "pip.tar file creation completed"
	else
			echo "pip.tar file creation failed"
			exit 1
	fi

	sleep 1

	# 5. Create install_sdk.sh script
	echo "============================================================================"
	echo "Creating install_sdk.sh script"
	echo "============================================================================"

	install_script_content="#!/bin/bash
	set -Eeuo pipefail
	trap 'echo \"[ERR] \$BASH_SOURCE:\$LINENO: command failed\"; exit 1' ERR

	echo \"============================================================================\"
	echo \"rebellion sdk install\"
	echo \"============================================================================\"

	echo \"compiler sdk version : ${compiler_version}\"
	echo \"optimum sdk version : ${optimum_version}\"
	echo \"vllm sdk version : ${vllm_version}\"

	echo \"\"
	echo \"tar -xf pip.tar\"
	mkdir -p ./pip
	tar -xf pip.tar -C ./pip

	echo \"\"
	echo \"rebellion compiler install\"
	sleep 3
	pip install ./pip/$(basename "${compiler_sdk_file}") -f ./pip --no-index

	echo \"\"
	echo \"optimum install\"
	sleep 3
	pip install ./pip/$(basename "${optimum_sdk_file}") -f ./pip --no-index

	echo \"\"
	echo \"vllm install\"
	sleep 3
	pip install ./pip/$(basename "${vllm_sdk_file}") -f ./pip --no-index

	rm -rf ./pip

	echo \"\"
	echo \"============================================================================\"
	echo \"pip install complete\"
	echo \"============================================================================\"
	"

	echo "$install_script_content" > "${NFS_SDK_PATH}/install_sdk.sh"
	chmod +x "${NFS_SDK_PATH}/install_sdk.sh"

	echo "install_sdk.sh script creation completed"

	# 6. Create final tar file
	echo "============================================================================"
	echo "Creating final SDK package"
	echo "============================================================================"

	
	cmd="tar -cf ${NFS_SDK_PATH}/${final_tar_name} -C ${NFS_SDK_PATH} pip.tar install_sdk.sh"

	echo "Executing command: $cmd"

	if eval "$cmd"; then
			echo "Final SDK package creation completed: $final_tar_name"
	else
			echo "Final SDK package creation failed"
			exit 1
	fi

	sleep 1

	# 7. Clean up temporary files
	echo "============================================================================"
	echo "Cleaning up temporary files"
	echo "============================================================================"

	cmd="rm -rf ${NFS_SDK_PATH}/pip ${NFS_SDK_PATH}/pip.tar ${NFS_SDK_PATH}/install_sdk.sh"
	echo "Deleting temporary files..."

	if eval "$cmd"; then
			echo "Temporary file cleanup completed"
	else
			echo "Some temporary file cleanup failed"
	fi

	echo "============================================================================"
	echo "SDK download and packaging completed"
	echo "============================================================================"
	echo "Created file: ${NFS_SDK_PATH}/${final_tar_name}"
	echo "Now you can transfer ${final_tar_name} to the target system and run install_sdk.sh."

	deactivate

done


"""


with open("download", "r", encoding="utf-8") as f:
    r = f.read()
   

    ## 문서내에서 치환
    r = r.replace("{{ DEFAULT_PATH }}", DEFAULT_PATH)
    r = r.replace("{{ NFS_SDK_PATH }}", NFS_SDK_PATH)
    r = r.replace("{{ REBELLIONS_ID }}", REBELLIONS_ID)
    r = r.replace("{{ REBELLIONS_PW }}", REBELLIONS_PW)
    r = r.replace("{{ PYTHON_VERSIONS }}", str(PYTHON_VERSIONS))
    
    
with open("download.sh", "w", encoding="utf-8") as f:
    f.write(r)

# Windows에서는 chmod가 필요하지 않음
if os.name != 'nt':  # Unix/Linux/Mac
    os.system("chmod +x download.sh")


print("sdk_init.sh, download.sh create complete")