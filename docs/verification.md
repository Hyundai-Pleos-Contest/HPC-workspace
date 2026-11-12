# 초기 세팅 검증

초기 구성에서 실제 실행한 결과다. 이후 변경의 성공 여부는 해당 커밋의 CI와 필요한 로컬 검사로 확인한다.

| 항목 | 상태 |
| --- | --- |
| 공통 문서와 Claude 가져오기 참조 | 네 저장소 기준본 일치, 로컬 문서 링크, @AGENTS.md 대상 존재 확인 |
| Android mock 빌드/검사 | Debug/Release APK 생성, Android Lint 오류 0. 단위 테스트는 아직 NO-SOURCE |
| Pleos SDK 배포 접근 | Vehicle 2.3.2 POM·AAR 공개 다운로드와 공식 SHA-256 일치 확인. 이전 2.3.1 POM 404와 구분 |
| Pleos 앱·계측 APK | Debug 앱 및 읽기 전용 계측 APK 빌드, Android Lint 오류 0. release manifest에 테스트용 CAR_DOORS 없음 |
| 실제 Pleos SDK 연결 | 전용 Pleos AVD의 Vehicle Service 2.3.22에서 capability 및 비-null 도어 상태 콜백 수신. 직접 adb·Gradle 계측 각각 1개 테스트 통과 |
| Pleos 앱 실행 | 현재 사용자에게 APK 설치·Launcher intent 실행 후 HPC 초기 화면과 visible 상태 확인 |
| BE 로컬 검사/실행 | Gradle 8.14.6 spotlessCheck/test/bootJar 성공, JUnit 1개 통과, JAR health HTTP 200 |
| AI 로컬 검사/실행 | uv lock, Ruff check/format 통과, pytest 5개 통과, CLI health HTTP 200 |
| Docker 통합 실행 | BE·AI 이미지 빌드, PostgreSQL 17.11 연결, Flyway 초기화, 두 서버 health HTTP 200 확인 |
| GitHub 병합 설정 | 네 저장소 merge commit 활성화, squash/rebase·자동 브랜치 삭제 비활성화 |
| GitHub 브랜치 보호 | 현재 Free 조직의 private 저장소에서 API 403. 보호 규칙 미적용 |
| Codex 새 세션 실제 로딩 | 설치된 CLI가 기본 모델을 지원하지 않아 응답 검증 미완료 |
| Claude 새 세션 실제 로딩 | 사용자 요청으로 보류. 파일 가져오기 참조만 확인 |

## 원격 CI
CI workflow는 각 저장소의 verify job으로 실행한다. 아래 페이지에서 실행 커밋과 결과를 확인한다.
- [Workspace CI](https://github.com/Hyundai-Pleos-Contest/HPC-workspace/actions/workflows/ci.yml)
- [Android CI](https://github.com/Hyundai-Pleos-Contest/HPC-fe/actions/workflows/ci.yml)
- [BE CI](https://github.com/Hyundai-Pleos-Contest/HPC-be/actions/workflows/ci.yml)
- [AI CI](https://github.com/Hyundai-Pleos-Contest/HPC-ai/actions/workflows/ci.yml)

## 환경 메모
- Android의 AAPT2 한글 경로 경고가 있었지만 두 APK 빌드는 성공했다.
- BE의 Windows 한글 경로 worker 문제는 Gradle JVM의 COMPAT 인코딩과 Java 소스·테스트 UTF-8 설정 분리로 해결했다.
- 검증용 SDK·캐시·실행 로그·APK는 Git에서 제외했다. SDK 전역 경로는 변경하지 않았다.
- 로컬 통합 검증은 임시 호스트 포트에서 수행했다. 컨테이너는 검증 후 종료하고 개발 DB 볼륨은 보존했다.

## Docker 빠른 시작 재검증 — 2026-11-10

- Docker Engine 29.6.1 / Compose 5.2.0에서 문서의 DB만 → BE 추가 → AI 추가 순서를 실행했다.
- 기존 8080 서비스와 충돌하지 않도록 별도 Compose 프로젝트와 호스트 포트 54322/18080/18000을 사용했다.
- PostgreSQL `healthy`·`pg_isready`, BE HTTP 200 `{"status":"UP"}`, AI HTTP 200 `{"status":"ok","service":"hpc-ai"}`를 확인했다.
- 기존에 빌드·검증한 이미지를 재사용했다. 이번 문서 검증에서는 이미지를 새로 빌드하지 않았다.
- `ps`, `logs`, `down`과 DB 볼륨 보존을 확인한 뒤 이번 검증용 볼륨만 정리했다. 기존 사용자 컨테이너와 DB는 유지했다.
- 현재 PC용 개인 `.env`는 BE 18080 / AI 18000 / DB 54322로 준비했다. 실제 `hpc-dev` 환경에서도 health를 확인하고 `down`으로 종료했으며 개발 DB 볼륨은 보존했다.
- Pleos 에뮬레이터에서 `10.0.2.2:18080/actuator/health`에 HTTP 200으로 접근했다. 이는 네트워크 경로 확인이며 앱의 BE 호출 기능은 아직 없다.

## Pleos 런타임 검증 — 2026-11-10

- Windows / WHPX, Android Emulator 37.1.11, Pleos Connect 2.1 API 34 x86_64 이미지에서 확인했다.
- 공식 이미지 ZIP SHA-1 `b4f858d5bcc6c71506d7edfc872bcb9e5a11acaa`와 다운로드 파일이 일치했고 ZIP CRC 검사 후 설치했다.
- 성공 구성은 새 AVD, RAM 4096 MB, Cold boot(`-no-snapshot`), `-gpu software`다. SDK·AVD는 프로젝트 로컬에 두고 네이티브 부팅 파일이 읽힐 수 있도록 영문 경로 Junction을 사용했다.
- Vehicle SDK 2.3.2 / Vehicle Service 2.3.22(code 74)에서 직접 adb 계측 `OK (1 test)`와 `position=0` 조회 콜백을 확인했다. 실제 차량을 조회한 결과는 아니다.
- `ANDROID_SERIAL`로 대상을 고정한 Gradle `connectedPleosDebugAndroidTest`도 1개 테스트가 통과했다. `--serial` 작업 옵션은 사용하지 않는다.
- APK를 다시 설치하고 `am start --user current`의 Launcher intent로 실행했다. 현재 사용자 10의 앱이 visible 상태이며 HPC 초기 화면이 표시되는 것을 캡처로 확인했다.
- 초기 AVD/host renderer 구성에서는 서비스 조회·설치 대기가 관찰됐다. 새 AVD/software 구성에서 통과했으며 하드웨어 렌더러 자체가 원인이라고 단정하지 않는다.
- headless 검증으로 앱 실행·SDK 조회를 확인했다. 실제 차량, 주행 중 동작, 멀티디스플레이 적합성은 이번 범위에 포함되지 않는다.

## 공용 실행 도구·새 clone 검증 — 2026-11-12

네 저장소를 별도 빈 부모 폴더에 Git clone해 검사했다. 기존 `.env`, `.local`,
`local.properties`, 프로젝트 빌드 산출물과 Gradle 캐시는 복사하지 않았다.
검증 절차는 [공용 로컬 도구](local-tools.md)에 기록했다.

| 소스 | 검증 기준 커밋 |
| --- | --- |
| HPC-workspace 공용 도구 | `5aa41f7` |
| HPC-fe 공용 도구 | `ea9bf5e` (초기 APK 빌드는 `96e5b53`, 이후 변경은 Python URL 검증과 해당 테스트뿐) |
| HPC-be | `8eef9c3` |
| HPC-ai | `ef7210a` |

- Windows / Python 3.12.12에서 workspace 도구 검사 3개, FE 도구 검사 5개가 통과했다.
- 네 저장소 공통 정책과 Markdown 참조 검사, diff 공백 검사를 통과했다.
- Android는 새 빈 `GRADLE_USER_HOME`에서 Gradle/의존성을 다운로드했다.
  Pleos 앱·계측 APK와 Lint가 6분 52초에 통과했고 75개 작업이 실행됐다.
- SDK와 Pleos AVD는 기존 설치를 명시적으로 전달했다. SDK/이미지 설치가 없는 새 PC 검증은 아니다.
- 공용 `start`로 Pleos API 34 AVD를 cold boot하고 `test`에서 실제 Vehicle SDK 계측
  1개가 3.898초에 통과했다. `launch` 후 현재 사용자 10의 `visible=true`를 확인하고 `stop`으로 종료했다.
- 직접 adb 계측 stdout 로그를 로컬에 보관했다. 실제 차량 검증과 구분한다.
- Docker Engine 29.6.1 / Compose 5.2.0에서 `init → doctor → up --stack all → status → health → down`을 실행했다.
  프로젝트 `hpc-repro-20261112`, DB 25432 / BE 28080 / AI 28000으로 기존 개발 환경과 분리했다.
- PostgreSQL healthy, BE `{"status":"UP"}`, AI `{"status":"ok","service":"hpc-ai"}`를 확인했다.
  AI 이미지는 Docker 레이어 캐시를 재사용했고, BE는 새 기본 이미지와 Gradle 의존성을 다운로드해 bootJar를 다시 빌드했다.
  Docker 전체 캐시를 지운 빌드로 표현하지 않는다.
- 테스트 DB에 임시 행을 저장한 뒤 공용 `down`과 `up --stack database`를 실행했다.
  PostgreSQL만 실행됐으며 기존 행 1개가 유지됨을 확인했다. 개발자의 원래 `.env`는 수정하지 않았다.
- 검증 후 컨테이너를 종료하고 소유 라벨을 확인한 임시 테스트 볼륨만 정리했다.
  기존 `hpc-dev_postgres-data`와 다른 프로젝트의 실행 중인 컨테이너는 유지했다.
- Docker 시작 시 WSL 데이터 디스크 연결 오류가 있었다. 실패한 Docker 프로세스와 전용 WSL 인스턴스를
  종료 후 다시 시작해 복구했고, 데이터 초기화·가상 디스크 삭제·다른 WSL 배포판 종료는 하지 않았다.
- Claude 실제 지침 로딩 검사는 기존 사용자 요청에 따라 계속 보류했다.
