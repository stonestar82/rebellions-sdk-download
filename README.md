# Rebellions SDK Download

리벨리온 SDK 신규 버전 체크 및 자동 다운로드 도구입니다.

## 📋 개요

이 프로젝트는 [리벨리온 공식 문서](https://docs.rbln.ai/latest/ko/supports/release_note.html)에서 최신 SDK 버전 정보를 자동으로 크롤링하고, 새로운 버전이 있을 경우 자동으로 다운로드하는 스크립트입니다.

## 🚀 주요 기능

- **자동 버전 체크**: 리벨리온 공식 문서에서 최신 릴리즈 정보 자동 수집
- **스마트 다운로드**: 기존 버전과 비교하여 새로운 버전만 다운로드
- **파일 관리**: 이전 버전 파일 자동 정리 및 백업
- **에러 처리**: 다운로드 실패 시 자동 에러 로깅

## 📁 프로젝트 구조

```
rebellions-install/
├── README.md                    # 프로젝트 설명서
├── req.txt                      # Python 패키지 의존성
├── sdk_common.py                # 공통 설정 및 상수
├── sdk_crawling.py              # 메인 크롤링 스크립트
├── sdk_init.py                  # 초기화 및 스크립트 생성 스크립트
├── sdk_docker.py                # Dockerfile 생성 스크립트
├── rebellions_container.sh      # Docker 컨테이너 빌드 및 패키징 스크립트
├── dockerfile_template          # Dockerfile 템플릿
├── docker_run.sh                # Docker 컨테이너 실행 스크립트
└── resnet_test.sh               # ResNet 테스트 스크립트
```

## ⚙️ 환경 설정

### sdk_common.py 설정 항목

| 설정 항목         | 설명                   | 예시                                 |
| ----------------- | ---------------------- | ------------------------------------ |
| `DEFAULT_PATH`    | 실행 소스 경로         | `/workspace/rebellions-sdk-download` |
| `NFS_SDK_PATH`    | SDK 파일 저장 경로     | `/srv/nfs/share/SDK`                 |
| `REBELLIONS_ID`   | 리벨리온 계정 ID       | `your_id`                            |
| `REBELLIONS_PW`   | 리벨리온 계정 비밀번호 | `your_password`                      |
| `PYTHON_VERSIONS` | 지원 Python 버전       | `"3.9" "3.10" "3.11"`                |

## 🎯 사용 방법

### 1. Docker 컨테이너 빌드 및 패키징

```bash
./rebellions_container.sh
```

**동작 과정:**

1. NFS 경로에서 Dockerfile 및 release_info.txt 확인
2. 기존 ubuntu-rebellions 이미지 삭제
3. release_info.txt에서 버전 정보 추출
4. Docker 이미지 빌드 (`ubuntu-rebellions:<version>`)
5. Docker 이미지를 tar 파일로 저장
6. docker_run.sh 및 docker_load.sh 스크립트 생성
7. 최종 패키지 압축 (`ubuntu-rebellions-complete.<version>.tar.gz`)

**생성되는 파일들:**

- `ubuntu-rebellions-complete.<version>.tar.gz`: 최종 배포 패키지
  - `ubuntu-rebellions.<version>.tar`: Docker 이미지
  - `docker_run.sh`: 컨테이너 실행 스크립트
  - `docker_load.sh`: 이미지 로드 스크립트

### 2. Docker 컨테이너 실행

```bash
# 이미지 로드
./docker_load.sh

# 컨테이너 실행 (디바이스 개수 지정: 1-16)
./docker_run.sh 4
```

**Docker 실행 옵션:**

- `--device /dev/rsd0`: 시스템 디바이스
- `--device /dev/rbln0 ~ /dev/rbln15`: 리벨리온 디바이스 (지정된 개수만큼)
- `--volume /usr/local/bin/rbln-stat:/usr/local/bin/rbln-stat`: 통계 도구
- `--volume /root/.cache:/root/.cache`: 캐시 디렉토리

### 3. 초기 설정 (최초 1회)

```bash
python sdk_init.py
```

**생성되는 파일들:**

- `sdk_init.sh`: Python 가상환경 생성 스크립트
- `download.sh`: SDK 다운로드 및 패키징 스크립트

**동작 과정:**

1. Python 3.9, 3.10, 3.11 버전별 가상환경 생성
2. 각 가상환경에 필요한 패키지 설치 (`req.txt` 기반)
3. SDK 다운로드 및 설치 스크립트 생성

### 4. 가상환경 초기화

```bash
./sdk_init.sh
```

**동작 과정:**

1. Python 3.9, 3.10, 3.11 버전별 가상환경 생성
2. 각 가상환경에 `req.txt`의 패키지 설치
3. 가상환경별 Python 및 pip 버전 확인

### 5. 자동 실행 (권장)

```bash
python sdk_crawling.py
```

**동작 과정:**

1. 리벨리온 릴리즈 노트 페이지 크롤링
2. 최신 버전 정보 추출 (릴리즈 날짜, 드라이버, 컴파일러, Optimum, VLLM 버전)
3. 릴리즈 정보 파일 생성

**생성되는 파일 예시:**

```bash
-rw-r--r-- 1 root root 113 Aug 20 12:46 release_2025.07.31.0_v1.3.73_0.8.2_0.8.2_0.8.2.txt
-rw-r--r-- 1 root root 108 Aug 20 12:46 release_info.txt
```

**release_info.txt 내용:**

```
release=2025.07.31.0
driver_version=v1.3.73
compiler_version=0.8.2
optimum_version=0.8.2
vllm_version=0.8.2
```

### 6. SDK 다운로드

```bash
./download.sh
```

`release_info.txt` 파일을 읽어서 컴파일러, Optimum, VLLM 버전을 확인하여 SDK를 다운로드합니다.

**특정 버전을 다운로드하려는 경우:**

```bash
./download.sh 0.8.2 0.8.2 0.8.2
```

**동작 과정:**

1. 지정된 버전의 Compiler, Optimum, VLLM SDK 다운로드
2. Python 버전별 가상환경에서 SDK 설치 테스트
3. 최종 패키지 생성 (`rebellions_sdk_python-<version>_compiler-<version>_optimum-<version>_vllm-<version>.tar`)

## 📊 출력 파일

### 생성되는 스크립트

- **`sdk_init.sh`**: Python 가상환경 초기화 스크립트
- **`download.sh`**: SDK 다운로드 및 패키징 스크립트

### 릴리즈 정보 파일

- **`release_<날짜>_<드라이버>_<컴파일러>_<optimum>_<vllm>.txt`**: 상세 릴리즈 정보
- **`release_info.txt`**: 간단한 릴리즈 정보 (컴파일러, Optimum, VLLM 버전 포함)

### SDK 패키지 파일

- **형식**: `rebellions_sdk_python-<python-version>_compiler-<컴파일러>_optimum-<optimum>_vllm-<vllm>.tar`
- **내용**:
  - `pip.tar`: 다운로드된 SDK wheel 파일들
  - `install_sdk.sh`: 타겟 시스템에서 실행할 설치 스크립트

## 🔧 의존성

- Python 3.9, 3.10, 3.11
- `beautifulsoup4`: HTML 파싱
- `jinja2`: 템플릿 엔진 (초기화용)

## 🌐 플랫폼 지원

### Linux 전용

현재 Linux 환경에서만 지원됩니다.

## 📝 로그 및 에러

- **성공 시**:
  - 가상환경 생성 완료
  - 릴리즈 정보 파일 생성
  - SDK 다운로드 및 패키징 완료
- **실패 시**: `crawling_error` 파일에 에러 정보 저장
- **중복 실행 시**: 기존 파일 존재 확인 후 중단

## 🔄 워크플로우

1. **초기값 설정**: `sdk_common.py`에 필요한 값들을 지정
2. **초기 설정**: `python sdk_init.py`로 스크립트 생성
3. **가상환경 생성**: `./sdk_init.sh`로 Python 환경 준비
4. **버전체크**: `python sdk_crawling.py`로 버전 체크
5. **SDK 다운로드**: `./download.sh`로 SDK 패키징

## 🤖 자동화

정기적인 SDK 버전 체크와 다운로드를 위해 cron 작업을 설정할 수 있습니다.

### Crontab 설정 예시

```bash
# 매일 오전 2시에 SDK 버전 체크
0 2 * * * root /usr/bin/python3 /workspace/rebellions-sdk-download/sdk_crawling.py

# 매일 오전 2시 5분분에 SDK 다운로드 (새로운 버전이 있을 경우)
5 2 * * * root /usr/bin/bash /workspace/rebellions-sdk-download/download.sh

```

### 자동화 시 고려사항

- **로그 관리**: cron 실행 결과를 로그 파일로 저장
- **에러 처리**: 실패 시 알림 설정 (이메일, 슬랙 등)
- **리소스 관리**: 동시 실행 방지를 위한 lock 파일 사용
- **백업**: 다운로드된 SDK 파일의 정기적인 백업

### 로그 설정 예시

```bash
# cron 작업에 로그 추가
0 2 * * * root /usr/bin/python3 /workspace/rebellions-sdk-download/sdk_crawling.py 2> /var/log/rebellions_sdk
```

## 📄 라이선스

이 프로젝트는 리벨리온 SDK 사용을 위한 아이클라우드(주) 내부 도구입니다.
