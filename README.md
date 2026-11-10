# HPC Workspace

현대자동차그룹 Pleos 차량용 Android 앱 프로젝트의 공통 협업·로컬 실행 저장소다.
이 저장소는 서비스 코드 대신 저장소 간 연결, 개발 시작 절차와 통합 설정을 관리한다.

## 저장소

아래 저장소를 같은 부모 폴더에 clone한다. 부모 폴더 자체는 Git 저장소로 만들지 않는다.

| 저장소 | 역할 |
| --- | --- |
| [HPC-fe](https://github.com/Hyundai-Pleos-Contest/HPC-fe) | Kotlin Android 앱, Pleos 접근 |
| [HPC-be](https://github.com/Hyundai-Pleos-Contest/HPC-be) | Java 21 Spring Boot API, DB 계약 |
| [HPC-ai](https://github.com/Hyundai-Pleos-Contest/HPC-ai) | Python 개발 환경, 선택적 내부 AI API |
| [HPC-workspace](https://github.com/Hyundai-Pleos-Contest/HPC-workspace) | 공통 규칙, 통합 Compose, 환경 안내 |

각 서비스의 단독 실행과 검사는 해당 저장소 README가 원본이다.

## 처음 시작하기

1. [환경 준비와 실행](docs/development.md)을 따라 필요한 도구와 저장소를 준비한다.
2. [협업 규칙](CONTRIBUTING.md)을 확인한다. 일반 작업은 develop에서 분기한다.
3. 변경하는 저장소에서 Codex 또는 Claude Code를 시작한다. 각 루트 AGENTS.md가 공통 지침이다.
4. 전체 관계는 [아키텍처](docs/architecture.md), 초기 범위는 [기술 결정](docs/decisions/0001-bootstrap.md)을 읽는다.

## 로컬 인프라

Docker Desktop의 Linux 컨테이너 엔진과 Docker Compose가 필요하다.
아래 명령은 HPC-workspace에서 실행한다. 기본 값은 개발용이며 외부 배포용이 아니다.

```powershell
Copy-Item .env.example .env
docker compose up -d postgres
docker compose --profile backend up -d --build
docker compose --profile backend --profile ai up -d --build
```

각 줄은 실행 범위를 선택하는 예시다. DB만 필요한 경우 첫 up 명령으로 충분하다.
AI는 외부 키 없이 health 응답만 제공하는 선택적 기본 서비스다.

- BE: http://localhost:8080/actuator/health
- AI: http://localhost:8000/health
- Android 에뮬레이터의 BE 주소: http://10.0.2.2:8080/
- 종료: `docker compose --profile backend --profile ai down` (DB 볼륨 보존)

포트와 실행 방법은 [개발 안내](docs/development.md)에 설명되어 있다.

## 검증

Python 3.12 이상과 Docker Compose를 사용한다. 이 저장소에는 Python 패키지 설치가 필요 없다.

```powershell
python scripts/check.py
python scripts/check.py --siblings
docker compose --profile backend --profile ai config --quiet
```

`--siblings`는 형제 저장소 네 곳의 공통 정책 일치와 AI 진입 문서를 검사한다.
CI는 workspace 자체와 Compose 구문을 검사한다. 서비스 빌드는 각 레포 CI가 담당한다.

## 문서

- [GitHub 초기 구성](docs/github-setup.md)
- [공모전·SDK 확인 사항](docs/pleos.md)
- [검증 상태](docs/verification.md)
- [통합 버전 기록 방법](docs/releases.md)
- [공통 설정 기준본](templates/common/CONTRIBUTING.md)

공통 파일 변경은 templates/common 기준본과 네 저장소 사본에 함께 반영한 후
`python scripts/check.py --siblings`로 확인한다.
