# 초기 개발환경 결정

상태: 초기 세팅 기준. 기능 개발 중 근거가 생기면 새 결정 문서로 변경한다.

## 선택
- FE: Kotlin Android 앱과 Compose. Pleos SDK 접근은 앱 내부 경계로 분리한다.
- BE: Java 21 + Spring Boot 단일 애플리케이션. DB가 필요하면 PostgreSQL + Flyway를 사용한다.
- AI: Python 3.12 + uv + Ruff + pytest. FastAPI health 골격은 선택 profile로 실행한다.
- 통합: Docker Compose. CI는 GitHub Actions, 버전 고정은 Wrapper/lockfile로 관리한다.
- Git: main/develop 기반 Git Flow, merge commit, 초기 리뷰 인원은 팀 구성 후 설정.
- AI 지침: 각 루트 AGENTS.md 원본 + CLAUDE.md의 @AGENTS.md 가져오기.

## 이유
차량용 앱의 빌드와 SDK 가용성을 일찍 확인하고, BE 업무와 Python 실험 환경을 독립적으로 관리한다.
초기에는 실행 가능성과 재현성에 필요한 구성만 준비한다.

## 이번 범위
공통 문서·프로젝트 골격·health 확인·빌드/검사·CI·로컬 통합 설정.

## 후속 결정
서비스 기능, 사용자 인증, 도메인 DB 스키마, 실제 AI 모델과 제공자,
유료 클라우드 배포, Android release 서명과 최종 package ID는 기능·배포 계획에서 확정한다.
