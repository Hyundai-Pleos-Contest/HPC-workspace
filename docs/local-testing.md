# Docker 로컬 테스트 빠른 시작

PostgreSQL과 BE를 띄우고 상태 응답을 확인하는 절차다. AI는 필요할 때 추가한다. 아래 Docker 명령은 PowerShell과 Linux/macOS에서 동일하며, **`HPC-workspace` 폴더에서 실행**한다.

## 1. 준비

- Git과 실행 중인 Docker 엔진, Docker Compose가 필요하다. Windows/macOS에서는 Docker Desktop의 Linux 컨테이너 엔진을 사용한다.
- Docker로 BE/AI를 실행할 때 호스트에 Java·Python·Gradle을 따로 설치할 필요는 없다. Android 앱 개발 도구는 [HPC-fe README](https://github.com/Hyundai-Pleos-Contest/HPC-fe#readme)를 따른다.
- 첫 빌드는 이미지·의존성을 내려받으므로 인터넷 연결과 시간이 필요하다.

```sh
docker version
docker compose version
```

`docker version`에 Server 정보까지 나와야 한다. 연결 오류가 나면 Docker Desktop/엔진을 먼저 시작한다. Linux의 Docker 접근 권한은 팀의 설치 절차에 따라 설정한다.

저장소는 다음과 같이 형제 폴더로 둔다. 이미 clone했다면 다시 받을 필요가 없다.

```text
HPC/
├── HPC-workspace/
├── HPC-fe/
├── HPC-be/
└── HPC-ai/
```

새 작업 폴더에서 받을 때는 두 운영체제 모두 다음 명령을 사용한다.

```sh
git clone https://github.com/Hyundai-Pleos-Contest/HPC-workspace.git
git clone https://github.com/Hyundai-Pleos-Contest/HPC-fe.git
git clone https://github.com/Hyundai-Pleos-Contest/HPC-be.git
git clone https://github.com/Hyundai-Pleos-Contest/HPC-ai.git
cd HPC-workspace
```

각 저장소는 테스트할 브랜치/커밋을 선택한다. Compose는 `../HPC-be`, `../HPC-ai`의 현재 소스를 빌드한다.

## 2. 개발 설정 복사

기존 `.env`가 없을 때만 예제를 복사한다. 이미 설정한 값은 덮어쓰지 않는다.

PowerShell:

```powershell
if (-not (Test-Path -LiteralPath .env)) { Copy-Item -LiteralPath .env.example -Destination .env }
```

Linux/macOS:

```sh
test -f .env || cp .env.example .env
```

기본 호스트 포트는 DB `5432`, BE `8080`, AI `8000`이다. 다른 앱이 사용 중이면 시작 전에 `.env`의 `POSTGRES_PORT`, `BE_PORT`, `AI_PORT`를 변경한다. 예를 들어 `BE_PORT=18080`이면 아래 BE 확인 주소도 `http://localhost:18080`으로 바꾼다. 기존 앱이나 컨테이너를 종료할 필요는 없다.

`.env`는 로컬 개발용이며 커밋하지 않는다. 예제 DB 계정은 `hpc` / `hpc-local-only`, DB 이름은 `hpc`다. Compose는 `.env`를 읽지만, IDE에서 직접 실행하는 Spring Boot나 Android 앱이 이 파일을 자동으로 읽지는 않는다.

## 3. 필요한 범위 실행

아래에서 필요한 **한 가지**를 선택한다. DB만 실행한 뒤 나중에 BE나 AI를 추가해도 된다.

| 범위 | 명령 |
| --- | --- |
| DB만 | `docker compose up -d --wait postgres` |
| DB + BE | `docker compose --profile backend up -d --build` |
| DB + BE + AI | `docker compose --profile backend --profile ai up -d --build` |

현재 Compose 프로젝트 이름은 `hpc-dev`다. 같은 프로젝트가 이미 실행 중인지 `docker compose --profile backend --profile ai ps`로 확인할 수 있다. 기존 환경과 완전히 분리해야 한다면 다른 호스트 포트와 `docker compose -p hpc-other ...`를 사용하고, 이후 상태·로그·종료 명령에도 같은 `-p`를 붙인다.

## 4. 상태 확인

DB 준비 상태:

```sh
docker compose --profile backend --profile ai ps
docker compose exec -T postgres pg_isready -U hpc -d hpc
```

DB 컨테이너는 `healthy`, `pg_isready`는 `accepting connections`가 정상이다. DB 사용자/이름을 바꿨다면 명령의 `hpc`도 해당 값으로 바꾼다.

BE/AI 컨테이너의 `Up` 표시는 프로세스 상태다. 다음 HTTP 응답까지 확인해야 서비스가 준비된 것이다. 기동 직후 연결 오류가 나면 몇 초 뒤 다시 실행한다. AI 확인은 AI를 실행한 경우만 필요하다.

PowerShell:

```powershell
Invoke-RestMethod http://localhost:8080/actuator/health
Invoke-RestMethod http://localhost:8000/health
```

Linux/macOS:

```sh
curl --fail http://localhost:8080/actuator/health
curl --fail http://localhost:8000/health
```

예상 JSON은 BE `{"status":"UP"}`, AI `{"status":"ok","service":"hpc-ai"}`이다. PowerShell은 같은 내용을 객체 표로 표시한다. 변경한 호스트 포트가 있으면 URL에 반영한다.

로그가 필요하면 다음 명령을 사용한다. 실시간 확인을 끝내는 `Ctrl+C`는 로그 표시만 종료한다.

```sh
docker compose --profile backend --profile ai logs --tail 100
docker compose --profile backend --profile ai logs -f backend
```

현재는 도메인 SQL migration이 없어 BE 로그의 Flyway `No migrations found` 경고가 나타날 수 있다. 초기 환경에서는 health가 `UP`인지 함께 확인한다.

## 5. 코드 수정과 종료

소스는 컨테이너에 자동 반영되지 않는다. BE 코드를 수정했다면 다음처럼 다시 빌드한다. AI만 바꿨다면 `docker compose --profile ai up -d --build ai`를 사용한다.

```sh
docker compose --profile backend up -d --build backend
```

테스트를 마치면 현재 프로젝트만 종료한다.

```sh
docker compose --profile backend --profile ai down
```

이 명령은 컨테이너·네트워크를 제거하고 **PostgreSQL 볼륨과 데이터는 보존**한다. 데이터 보존을 위해 `down`에 `-v`를 붙이지 않는다. 다시 `up`하면 기존 DB를 사용한다. 이미 생성된 DB의 사용자·비밀번호는 `.env`를 바꾼다고 자동 변경되지 않는다.

## Android / Pleos와 연결할 때

Android 에뮬레이터에서 개발 PC의 BE 주소는 `http://10.0.2.2:8080`이다. `BE_PORT=18080`을 썼다면 `http://10.0.2.2:18080`을 사용한다. 앱의 개발 주소는 **`HPC-fe` 폴더에서** 빌드할 때 지정한다.

PowerShell:

```powershell
.\gradlew.bat :app:assembleMockDebug -PapiBaseUrl=http://10.0.2.2:18080
```

Linux/macOS:

```sh
bash ./gradlew :app:assembleMockDebug -PapiBaseUrl=http://10.0.2.2:18080
```

`18080`은 포트를 변경한 예시다. 기본 포트를 쓰면 `8080`을 사용한다. 실제 기기는 `10.0.2.2`를 사용하지 않으며 별도 HTTPS 개발 주소가 필요하다. Compose의 호스트 포트는 `127.0.0.1`에만 열려 있다.

현재 BE와 AI는 상태 확인만 제공하며, BE→AI 호출과 Android→BE 기능은 아직 구현하지 않았다. 주소 설정이나 health 성공이 기능 통합 완료를 뜻하지 않는다. `mockDebug`는 차량 SDK 연결을 검증하지 않는다. Pleos SDK 접근 권한·API permission·에뮬레이터 설치와 실제 SDK 연결은 [Pleos 개발 환경 안내](pleos.md) 및 HPC-fe 문서에 따라 별도로 확인한다.
