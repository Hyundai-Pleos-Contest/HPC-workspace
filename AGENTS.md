# HPC-workspace 작업 지침

## 역할
- 이 저장소는 공통 규칙, 아키텍처, 로컬 통합 실행을 소유한다.
- Android, BE, AI 기능 코드는 각 저장소가 소유한다.
- 각 서비스 API 계약의 원본을 이곳에 중복 작성하지 않는다.
- 형제 저장소의 AGENTS.md가 자동 상속된다고 가정하지 않는다. 다른 저장소를 수정할 때 해당 지침을 읽는다.

## 작업 전 확인
- 브랜치·커밋·PR 작업 전에 CONTRIBUTING.md를 읽는다.
- 통합 실행 변경은 docs/development.md와 compose.yaml을 확인한다.
- 경계·기술 변경은 docs/architecture.md와 docs/decisions/0001-bootstrap.md를 확인한다.
- 공모전·SDK 판단은 docs/pleos.md에 연결된 공식 자료를 다시 확인한다.

## 검증 명령
저장소 루트에서 실행한다.
- `python scripts/check.py`: workspace 공통 정책·문서 확인.
- `python scripts/check.py --siblings`: 형제 레포까지 공통 정책과 AI 진입 문서 확인.
- `docker compose --profile backend --profile ai config --quiet`: 통합 설정 구문 확인.
- `python -m unittest discover -s scripts -p "test_*.py"`: 공용 실행 스크립트의 설정·DB 보존 검사.
- 로컬 실행은 docs/local-tools.md의 `python scripts/dev.py`를 사용한다. 별도 검증에서는 프로젝트 이름과 포트를 분리한다.
- 컨테이너 동작 변경 시 필요한 profile을 실행하고 실제 health 응답을 확인한다.

## 고유 규칙
- 서비스 Dockerfile은 서비스 저장소에, 통합 Compose는 이곳에 둔다.
- .env.example은 개발 예제다. 실제 .env와 비밀값은 커밋하지 않는다.
- 공통 정책은 templates/common에서 고친 뒤 네 저장소 사본에 동일하게 반영한다.
- 아직 실행하지 않은 검사나 실제 SDK 연결을 성공으로 보고하지 않는다.
- AGENTS.md에는 실제 정의된 명령만 기재한다. Claude 전용 가져오기는 CLAUDE.md에서만 사용한다.
