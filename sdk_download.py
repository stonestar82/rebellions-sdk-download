import sys
import requests
from datetime import datetime
import os, time
import glob
from jinja2 import Template
from sdk_common import NFS_SDK_PATH, REBELLIONS_ID, REBELLIONS_PW

print("============================================================================")
print("rebellion studio sdk downloader")
print("============================================================================")


## 외부 파라미터 체크 3개
compiler_version = sys.argv[1]
optimum_version = sys.argv[2]
vllm_version = sys.argv[3]


print(f"compiler_version: {compiler_version}")
print(f"optimum_version: {optimum_version}")
print(f"vllm_version: {vllm_version}")

time.sleep(1)

print("")
print("============================================================================")
print(f"compiler sdk download start : v{compiler_version}")
print("============================================================================")


cmd = f"pip3 download --extra-index-url https://{REBELLIONS_ID}:{REBELLIONS_PW}@pypi.rbln.ai/simple rebel-compiler=={compiler_version} -d {NFS_SDK_PATH}/pip"

# print(cmd)

## cmd 실행
os.system(cmd)

time.sleep(1)

## find compiler sdk file
## rebel_compiler-0.8.2-cp310-cp310-manylinux_2_28_x86_64.whl 정규식으로 찾기

compiler_sdk_file = glob.glob(f"{NFS_SDK_PATH}/pip/rebel_compiler-{compiler_version}-*.whl")

if len(compiler_sdk_file) == 0:
    print(f"compiler sdk file not found : {compiler_sdk_file}")
    exit()

print(f"compiler sdk file found : {compiler_sdk_file[0]}")
## 파일 이름 추출
compiler_sdk_file = compiler_sdk_file[0]

print("")
print("============================================================================")
print(f"optimum sdk download start : v{optimum_version}")
print("============================================================================")

cmd = f"pip3 download --extra-index-url https://{REBELLIONS_ID}:{REBELLIONS_PW}@pypi.rbln.ai/simple optimum-rbln=={optimum_version} -d {NFS_SDK_PATH}/pip"

# print(cmd)

## cmd 실행
os.system(cmd)

time.sleep(1)

## find optimum sdk file
## optimum_rbln-0.8.2-py3-none-any.whl 정규식으로 찾기
optimum_sdk_file = glob.glob(f"{NFS_SDK_PATH}/pip/optimum_rbln-{optimum_version}-*.whl")

if len(optimum_sdk_file) == 0:
    print(f"optimum sdk file not found : {optimum_sdk_file}")
    exit()
    
print(f"optimum sdk file found : {optimum_sdk_file[0]}")
optimum_sdk_file = optimum_sdk_file[0]

print("")
print("============================================================================")
print(f"vllm sdk download start : v{vllm_version}")
print("============================================================================")
cmd = f"pip3 download --extra-index-url https://{REBELLIONS_ID}:{REBELLIONS_PW}@pypi.rbln.ai/simple vllm-rbln=={vllm_version} -d {NFS_SDK_PATH}/pip"
# print(cmd)

## cmd 실행
os.system(cmd)
time.sleep(1)
## find vllm sdk file
## vllm_rbln-0.8.2-py3-none-any.whl 정규식으로 찾기
vllm_sdk_file = glob.glob(f"{NFS_SDK_PATH}/pip/vllm_rbln-{vllm_version}-*.whl")

if len(vllm_sdk_file) == 0:
	print(f"vllm sdk file not found : {vllm_sdk_file}")
	exit()

print(f"vllm sdk file found : {vllm_sdk_file[0]}")
vllm_sdk_file = vllm_sdk_file[0]


## tar 파일 생성
print("")
print("============================================================================")
print("tar file create start")
print("============================================================================")


cmd = f"tar -cf {NFS_SDK_PATH}/pip.tar {NFS_SDK_PATH}/pip/*"

print(cmd)

## cmd 실행
os.system(cmd)

time.sleep(1)


template = """
#!/bin/bash
set -Eeuo pipefail
trap 'echo "[ERR] $BASH_SOURCE:$LINENO: command failed"; exit 1' ERR

echo "============================================================================"
echo "rebellion sdk install"
echo "============================================================================"

echo "compiler sdk version : {{ COMPILER_VERSION }}"
echo "optimum sdk version : {{ OPTIMUM_VERSION }}"
echo "vllm sdk version : {{ VLLM_VERSION }}"

echo ""
echo "tar -xf pip.tar"
tar -xf pip.tar

echo ""
echo "rebellion compiler install"
sleep 3
pip install {{ COMPILER_SDK_FILE }} -f {{ NFS_SDK_PATH }}/pip --no-index

echo ""
echo "optimum install"
sleep 3
pip install {{ OPTIMUM_SDK_FILE }} -f {{ NFS_SDK_PATH }}/pip --no-index

echo ""
echo "vllm install"
sleep 3
pip install {{ VLLM_SDK_FILE }} -f {{ NFS_SDK_PATH }}/pip --no-index

echo ""
echo "============================================================================"
echo "pip install complete"
echo "============================================================================"


"""

t = Template(template)

data = {
	"COMPILER_VERSION": compiler_version,
	"OPTIMUM_VERSION": optimum_version,
	"VLLM_VERSION": vllm_version,
	"COMPILER_SDK_FILE": compiler_sdk_file,
	"OPTIMUM_SDK_FILE": optimum_sdk_file,
	"VLLM_SDK_FILE": vllm_sdk_file,
	"NFS_SDK_PATH": NFS_SDK_PATH
}


with open(f"{NFS_SDK_PATH}/install_sdk.sh", "w") as f:
    f.write(t.render(**data))

os.system(f"chmod +x {NFS_SDK_PATH}/install_sdk.sh")	



## pip.tar install_sdk.sh 압축
cmd = f"tar -cf {NFS_SDK_PATH}/rebellions_sdk_compiler-{compiler_version}_optimum-{optimum_version}_vllm-{vllm_version}.tar {NFS_SDK_PATH}/pip.tar {NFS_SDK_PATH}/install_sdk.sh"
print(cmd)

## cmd 실행
os.system(cmd)

time.sleep(1)

cmd = f"rm -rf {NFS_SDK_PATH}/pip {NFS_SDK_PATH}/pip.tar {NFS_SDK_PATH}/install_sdk.sh"
os.system(cmd)

print("")
print("============================================================================")
print(f"install_sdk.sh create complete")
print("============================================================================")
