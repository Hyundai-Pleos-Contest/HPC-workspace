# GitHub 초기 설정

## 기준
- 기본 브랜치 main, 개발 통합 develop.
- merge commit 허용, squash/rebase 병합 비활성화.
- release/hotfix 이중 반영을 위해 병합 시 원본 브랜치 자동 삭제 비활성화.
- main/develop은 PR 필수, 필수 CI 성공, 리뷰 대화 해결, force push/삭제 제한.
- merge commit과 충돌하는 linear history 요구는 사용하지 않는다.
- 리뷰 인원과 CODEOWNERS는 실제 팀 구성 후 결정한다.
- 초기 환경을 검증한 뒤 최초 baseline을 main에 커밋하고 develop을 같은 커밋에서 만든다.
- 일반 개발은 이후 develop에서 작업 브랜치를 만든다.

## CI
각 저장소 workflow의 이름은 CI, job ID는 verify다.
실제 GitHub 실행에서 성공한 check 이름을 확인한 후 필수 검사로 등록한다.
로컬 검사 통과와 GitHub 실행 성공을 구분한다.

## 권한과 플랜
비공개 조직 저장소의 브랜치 보호는 GitHub 플랜에 따라 지원 범위가 다르다.
적용 실패 시 문서만으로 강제된다고 보고하지 않고 검증 문서에 제한을 남긴다.
리뷰 승인 인원은 아직 설정하지 않는다.

현재 Hyundai-Pleos-Contest는 Free 조직이고 네 저장소는 private이다.
브랜치 보호 API가 플랜 업그레이드 또는 공개 저장소를 요구하며 HTTP 403을 반환했다.
따라서 보호 규칙은 아직 강제되지 않는다. 비공개 상태와 유료 플랜은 변경하지 않았다.
지원 환경으로 변경한 뒤 config/branch-protection.json을 main과 develop 각각에 적용할 수 있다.
필수 status check 이름 verify는 AI 저장소의 실제 성공한 GitHub job에서 확인했다.

merge commit 허용, squash/rebase 비활성화, 병합 후 브랜치 자동 삭제 비활성화는 네 저장소에 적용했다.

## AI 지침 확인
- Codex: 각 저장소를 루트로 새 세션을 열고 지침 출처를 확인한다.
- Claude Code: 새 세션에서 /context all 또는 /memory로 CLAUDE.md와 가져오기 내용을 확인한다.
- 파일 연결 검사와 런타임 컨텍스트 로딩 검증을 구분한다.
- 개인·조직의 설정을 자동으로 바꾸지 않는다.
