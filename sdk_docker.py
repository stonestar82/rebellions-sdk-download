from sdk_common import DEFAULT_PATH, NFS_SDK_PATH, ERROR_FILE_NAME, REBELLIONS_ID, REBELLIONS_PW, PYTHON_VERSIONS
import subprocess, os, shutil
from jinja2 import Template

with open(f"{NFS_SDK_PATH}/release_info.txt", "r", encoding="utf-8") as f:
	r = f.read()
	release_date = r.split("release=")[1].split("\n")[0].strip()
	compiler_version = r.split("compiler_version=")[1].split("\n")[0].strip()
	optimum_version = r.split("optimum_version=")[1].split("\n")[0].strip()
	vllm_version = r.split("vllm_version=")[1].split("\n")[0].strip()
	
	rebellions_sdk = f"rebellions_sdk_python-3.10_compiler-{compiler_version}_optimum-{optimum_version}_vllm-{vllm_version}.tar"
 
 
	cmd = "docker images --format '{{json .}}' | jq -r 'select(.Repository==\"ubuntu-rebellions\") | .Tag'"
 
	out = subprocess.run(cmd, encoding='utf-8', capture_output=True, text=True, shell=True)
	docker_tag = out.stdout.strip()
 
	if docker_tag != release_date:

		with open(f"{DEFAULT_PATH}/dockerfile_template", "r", encoding="utf-8") as f:
			template = f.read()
			
		t = Template(template)

		with open(f"{NFS_SDK_PATH}/Dockerfile", "w", encoding="utf-8") as f:
			f.write(t.render(REBELLIONS_SDK=rebellions_sdk))
   
		shutil.copy("resnet_test.sh", f"{NFS_SDK_PATH}/resnet_test.sh")

  
