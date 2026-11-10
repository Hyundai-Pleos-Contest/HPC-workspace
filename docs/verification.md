# 초기 세팅 검증

초기 구성에서 실제 실행한 결과다. 이후 변경의 성공 여부는 해당 커밋의 CI와 필요한 로컬 검사로 확인한다.

| 항목 | 상태 |
| --- | --- |
| 공통 문서와 Claude 가져오기 참조 | 네 저장소 기준본 일치, 로컬 문서 링크, @AGENTS.md 대상 존재 확인 |
| Android mock 빌드/검사 | Debug/Release APK 생성, Android Lint 오류 0. 단위 테스트는 아직 NO-SOURCE |
| Pleos SDK 배포 접근 | Vehicle 2.3.2 POM·AAR 공개 다운로드와 공식 SHA-256 일치 확인. 이전 2.3.1 POM 404와 구분 |
| Pleos 앱·계측 APK | Debug 앱 및 읽기 전용 계측 APK 빌드, Android Lint 오류 0. release manifest에 테스트용 CAR_DOORS 없음 |
| 실제 Pleos SDK 연결 | 전용 에뮬레이터에서 별도 검증 필요. 다운로드·컴파일 성공만으로 연결 성공을 판단하지 않음 |
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
