import requests
from bs4 import BeautifulSoup
import subprocess, os, glob
from sdk_common import DEFAULT_PATH, NFS_SDK_PATH

ERROR_FILE_NAME = "crawling_error"


try:

	### 리벨리온 릴리즈 크롤링
	url = "https://docs.rbln.ai/latest/ko/supports/release_note.html"

	response = requests.get(url)
	response.raise_for_status()

	html = BeautifulSoup(response.text, 'html.parser')

	# TOC 요소에서 첫 번째 링크의 href 값 찾기
	article = html.select_one("article.md-content__inner.md-typeset")

	# print(article)

	tbl = article.find("table")
	td = tbl.find_all("td")

	release_date = td[0].text.strip()
	driver_version = td[1].text.strip()
	compiler_version = td[2].text.strip().replace('v', '')
	optimum_version = td[3].text.strip().replace('v', '')
	vllm_version = td[4].text.strip().replace('v', '')

	file_name = f"release_{release_date}_{driver_version}_{compiler_version}_{optimum_version}_{vllm_version}.txt"

	if os.path.exists(f"{NFS_SDK_PATH}/{file_name}"):
		print(f"file already exists : {file_name}")
		exit()

	## release_*.txt 파일 찾기
	release_file = glob.glob(f"{NFS_SDK_PATH}/release_*.txt")

	if len(release_file) > 0:
		## 파일 삭제
		for file in release_file:
			os.remove(file)
		

	## 기존 SDK 삭제
	sdk_file = glob.glob(f"{NFS_SDK_PATH}/rebellions_sdk_*.tar")

	if len(sdk_file) > 0:
		## 파일 삭제
		for file in sdk_file:
			os.remove(file)




	with open(f"{NFS_SDK_PATH}/{file_name}", "w", encoding="utf-8") as f:
		f.write(f"release\t\t\t{release_date}\n")
		f.write(f"driver_version\t\t{driver_version}\n")
		f.write(f"compiler_version\t{compiler_version}\n")
		f.write(f"optimum_version\t\t{optimum_version}\n")
		f.write(f"vllm_version\t\t{vllm_version}\n")
  
  
	with open(f"{NFS_SDK_PATH}/release_info.txt", "w", encoding="utf-8") as f:
		f.write(f"release={release_date}\n")
		f.write(f"driver_version={driver_version}\n")
		f.write(f"compiler_version={compiler_version}\n")
		f.write(f"optimum_version={optimum_version}\n")
		f.write(f"vllm_version={vllm_version}\n")


	if os.path.exists(f"{NFS_SDK_PATH}/{ERROR_FILE_NAME}"):
 
		os.remove(f"{NFS_SDK_PATH}/{ERROR_FILE_NAME}")
 
	print(f"sdk_crawling complete")

except Exception as e:
	
	with open(f"{NFS_SDK_PATH}/{ERROR_FILE_NAME}", "w", encoding="utf-8") as f:
		f.write(f"{e}\n")

	exit()