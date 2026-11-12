# 공용 로컬 실행 도구

Python 3.12 이상 표준 라이브러리만 사용한다. Windows PowerShell과 Linux에서 같은 명령을
실행한다. Python 명령이 `python3`인 환경은 예제의 `python`을 바꾼다.
SDK·Docker 설치와 라이선스 동의는 개발자가 직접 진행한다.

## Docker 빠른 실행

[최초 clone·Docker 설치 준비](local-testing.md#1-준비)를 마친 뒤 `HPC-workspace`에서 실행한다.

```sh
python scripts/dev.py init
# .env의 포트를 검토하고 충돌하는 값은 변경한다.
python scripts/dev.py doctor
python scripts/dev.py up
python scripts/dev.py status
python scripts/dev.py health
python scripts/dev.py down
```

- `init`: `.env.example`을 복사한다. 기존 파일은 바꾸지 않는다.
- `doctor`: Docker Linux 엔진, Compose 설정, 필요한 형제 저장소를 확인한다.
- `up`: 소스에서 이미지를 빌드하고 컨테이너를 시작한 뒤 실제 health 응답까지 확인한다.
  Docker의 빌드 캐시는 사용할 수 있다. 최초 다운로드·빌드는 최대 30분 기다린다.
- `status`: 해당 프로젝트의 실행·종료 컨테이너를 표시한다.
- `health`: DB health와 BE/AI HTTP 응답을 검사한다. BE는 최대 90초 준비를 기다린다.
- `down`: 해당 프로젝트 전체를 종료한다. DB 볼륨과 이미지는 보존한다.

기본 범위는 **DB + BE**다. `doctor`, `up`, `health`에 같은 `--stack`을 사용한다.

| 옵션 | 범위 |
| --- | --- |
| `--stack database` | PostgreSQL |
| `--stack backend` | PostgreSQL + BE (기본) |
| `--stack all` | PostgreSQL + BE + AI |

```sh
python scripts/dev.py doctor --stack all
python scripts/dev.py up --stack all
python scripts/dev.py health --stack all
```

`up`의 범위를 줄여도 이미 실행 중인 다른 서비스는 자동으로 종료하지 않는다.
`status`와 `down`은 선택한 프로젝트의 모든 알려진 서비스에 적용된다.
실패 시 종료 코드가 0이 아니며, 진단을 위해 이미 시작된 컨테이너는 남긴다.
[원래 Compose 명령과 로그 확인](local-testing.md)도 계속 사용할 수 있다.

## 별도 테스트 환경

기존 개발 환경과 구분하려면 **프로젝트 이름과 포트를 모두** 분리한다.
상대 `--env-file` 경로는 `HPC-workspace` 기준이다. 실행 위치와 무관하게 같은 Compose 파일을 사용한다.

```sh
python scripts/dev.py init --env-file .env.verify
# .env.verify에서 POSTGRES_PORT, BE_PORT, AI_PORT를 비어 있는 별도 포트로 지정
python scripts/dev.py up --stack all --project hpc-verify --env-file .env.verify
python scripts/dev.py health --stack all --project hpc-verify --env-file .env.verify
python scripts/dev.py down --project hpc-verify --env-file .env.verify
```

세 명령에 동일한 `--project`와 `--env-file`을 전달한다. 실제 `.env.*`는 Git에서 제외된다.
Compose 규칙상 셸 환경변수가 env 파일보다 우선하므로 기존 `BE_PORT` 등의 셸 설정도 확인한다.
스크립트는 설정의 비밀번호를 출력하지 않으며 `down -v`나 전역 Docker 정리를 실행하지 않는다.

## Android와 연결

Pleos SDK/AVD 설치와 공용 명령은
[HPC-fe 로컬 도구](https://github.com/Hyundai-Pleos-Contest/HPC-fe/blob/develop/docs/local-tools.md)를 따른다.
`HPC-fe`의 `python scripts/pleos.py build --api-base-url http://10.0.2.2:<BE_PORT>`로
debug 서버 주소를 지정한다. Android는 workspace `.env`를 자동으로 읽지 않는다.
현재 앱에는 실제 BE 호출 기능이 없으므로 주소 설정과 서비스 간 연동 완성을 구분한다.

## 스크립트 검사

```sh
python -m unittest discover -s scripts -p "test_*.py"
python scripts/check.py --siblings
```

CI는 스크립트의 설정 보존·종료 범위 검사와 기존 문서/Compose 구문 검사를 실행한다.
Docker 통합 실행은 아직 CI에 포함하지 않는다.

## 새 clone에서 재현 확인

1. 빈 부모 폴더에 네 저장소의 `develop`을 형제 폴더로 clone한다.
2. 기존 `.env`, `.local`, `local.properties`, 빌드 산출물은 복사하지 않는다.
3. 이 문서의 `init → doctor → up → health → down`을 별도 프로젝트/포트로 실행한다.
4. Android는 미리 설치한 JDK/SDK/AVD를 명시하고 FE 로컬 도구 절차를 실행한다.
   Gradle 캐시까지 분리하려면 새 빈 폴더를 `GRADLE_USER_HOME`으로 지정한다.
5. 성공 여부와 사용한 소스 SHA, 운영체제, 캐시 사용 범위를 기록한다.

기존 Docker 레이어나 설치된 SDK를 재사용했다면 완전히 새로운 PC 설치 검증으로 표현하지 않는다.

## 도구 근거

- [Docker Compose up 및 wait](https://docs.docker.com/reference/cli/docker/compose/up/)
- [Docker Compose down의 볼륨 보존](https://docs.docker.com/reference/cli/docker/compose/down/)
