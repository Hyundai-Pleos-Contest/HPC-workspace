# 협업 규칙

공통 기준: `hpc-bootstrap-v1`. 기준본은 HPC-workspace의 `templates/common/CONTRIBUTING.md`이다.
공통 규칙을 바꾸면 기준본과 네 저장소의 사본을 같은 작업 묶음으로 갱신한다.
저장소별 실행·검사 명령은 해당 README와 빌드 설정이 원본이다.

## Git Flow

| 브랜치 | 출발 | PR 대상 | 목적 |
| --- | --- | --- | --- |
| main | 최초 초기 커밋 | — | 검증된 릴리스 |
| develop | main | — | 다음 버전 통합 |
| feature/<설명> | develop | develop | 기능 |
| fix/<설명> | develop | develop | 미릴리스 코드 수정 |
| chore/<설명>, docs/<설명> | develop | develop | 설정·문서 |
| release/<버전> | develop | main, develop | 릴리스 안정화 |
| hotfix/<버전> | main | main, develop | 릴리스 긴급 수정 |

- 브랜치 이름은 소문자 영문과 하이픈을 사용한다. 이슈 번호가 있으면 `feature/12-vehicle-state`처럼 넣는다.
- main과 develop에는 PR로 반영한다. 최초 빈 저장소의 검증된 초기 개발환경 커밋과 브랜치 생성은 예외다.
- 모든 PR은 merge commit으로 병합한다. 공유 브랜치 rebase/force push는 하지 않는다.
- release에는 새 기능을 추가하지 않는다. main과 develop 양쪽에 반영한 뒤 삭제한다.
- hotfix는 진행 중인 release에도 반영한다. 필요한 모든 반영이 끝날 때까지 원본 브랜치를 보존한다.
- 검증을 통과한 main 커밋에 `v0.1.0` 형식의 태그를 붙인다. 빌드 산출물은 해당 SHA와 연결한다.
- 기본 브랜치는 main이다. 일반 작업 PR은 develop을 대상으로 한다.
- develop 대상 PR의 `Closes #번호`만으로 GitHub 이슈가 자동 종료되지 않는다. 개발 완료 상태를 명시적으로 갱신한다.

## 커밋

`type(scope): 한국어 설명`을 사용한다. scope는 선택 사항이다.

- type: feat, fix, refactor, docs, test, build, ci, chore
- 예: `feat(vehicle): 차량 상태 조회 추가`, `ci: 기본 빌드 검사 구성`
- 하나의 목적을 설명하고 되돌릴 수 있는 단위로 커밋한다.
- 브랜치·타입·코드 식별자는 영문, 문서와 협업 설명은 한국어를 기본으로 한다.

## PR과 리뷰

- 목적, 주요 변경, 실제 검증 결과, 관련 이슈, 다른 레포 영향을 적는다.
- 실행하지 못한 검사는 이유를 적는다. 정의된 명령과 실행 성공을 구분한다.
- 기능·버그는 관련 이슈를 연결한다. 사소한 설정·문서 변경은 이슈가 없어도 된다.
- 다른 저장소 이슈는 `Hyundai-Pleos-Contest/저장소#번호`로 구분한다.
- 리뷰 인원과 CODEOWNERS는 실제 팀 구성 후 정한다. CI 통과와 리뷰 대화 해결을 기본 조건으로 한다.
- PR 작성자는 변경 범위에 맞는 README의 검사를 실행한다. 포맷·정적 검사는 도구 설정을 따른다.

## 여러 저장소의 변경

- 각 저장소는 독립 버전으로 관리한다.
- 공개 API 계약은 제공하는 서비스 저장소가 소유한다. 소비자와 HPC-workspace에서 독립적으로 복제 수정하지 않는다.
- 호환성을 깨는 변경은 제공자 확장 → 소비자 전환 → 이전 형식 제거 순서로 진행한다.
- 통합 실행 설정과 검증된 커밋·산출물 조합은 HPC-workspace에서 관리한다.
- SDK/모델의 실제 동작과 mock 결과를 구분한다.

## 환경과 데이터

- 비밀키, 개인 SDK 경로, 실제 .env, 서명 키, 개인정보·차량 원본 데이터는 커밋하지 않는다.
- 예제 설정에는 로컬 개발용 값 또는 명확한 placeholder만 사용한다.
- 대형 모델·데이터·빌드 산출물은 Git 이력에 넣지 않는다. 제출 APK는 소스 태그와 연결된 배포 위치로 안내한다.
- 공용 실행 절차는 Windows PowerShell과 Linux CI에서 재현할 수 있게 유지한다.
