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
├── README.md              # 프로젝트 설명서
├── sdk_common.py          # 공통 설정 및 상수
├── sdk_crawling.py        # 메인 크롤링 스크립트
└── sdk_download.py        # SDK 다운로드 스크립트
```

## ⚙️ 환경 설정

### sdk_common.py 설정 항목

| 설정 항목       | 설명                   | 예시              |
| --------------- | ---------------------- | ----------------- |
| `DEFAULT_PATH`  | 실행 소스 경로         | `/path/to/script` |
| `NFS_SDK_PATH`  | SDK 파일 저장 경로     | `/nfs/sdk`        |
| `REBELLIONS_ID` | 리벨리온 계정 ID       | `your_id`         |
| `REBELLIONS_PW` | 리벨리온 계정 비밀번호 | `your_password`   |

## 🎯 사용 방법

### 1. 자동 실행 (권장)

```bash
python3 sdk_crawling.py
```

**동작 과정:**

1. 리벨리온 릴리즈 노트 페이지 크롤링
2. 최신 버전 정보 추출 (릴리즈 날짜, 드라이버, 컴파일러, Optimum, VLLM 버전)
3. 기존 파일과 비교하여 새로운 버전 확인
4. 새로운 버전 발견 시 `sdk_download.py` 자동 실행
5. 다운로드 완료 후 릴리즈 정보 파일 생성

### 2. 수동 실행

```bash
python3 sdk_download.py <compiler-version> <optimum-version> <vllm-version>
```

**예시:**

```bash
python3 sdk_download.py 0.8.2 0.8.2 0.8.2
```

## 📊 출력 파일

### 릴리즈 정보 파일

- **형식**: `release_<날짜>_<드라이버>_<컴파일러>_<optimum>_<vllm>.txt`
- **내용**: 릴리즈 날짜, 드라이버 버전, 컴파일러 버전, Optimum 버전, VLLM 버전

### SDK 파일

- **형식**: `rebellions_sdk_compiler-<컴파일러>_optimum-<optimum>_vllm-<vllm>.tar`

## 🔧 의존성

- Python 3.x
- `requests`: HTTP 요청 처리
- `beautifulsoup4`: HTML 파싱
- `subprocess`: 외부 명령어 실행

## 📝 로그 및 에러

- **성공 시**: 릴리즈 정보 파일 생성 및 SDK 다운로드 완료
- **실패 시**: `crawling_error` 파일에 에러 정보 저장
- **중복 실행 시**: 기존 파일 존재 확인 후 중단

## 📄 라이선스

이 프로젝트는 리벨리온 SDK 사용을 위한 내부 도구입니다.
