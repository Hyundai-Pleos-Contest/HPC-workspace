# 공모전과 Pleos 확인 사항

프로젝트는 Pleos Connect에서 실행할 Android 앱이다. 웹 UI가 필요하면 별도 저장소를 검토한다.

## 공식 자료
- [공모전 공고](https://appdevchallenge.auto-hmg.io/notice/c0a1a000-2026-4923-8000-000000000001)
- [공모전 FAQ](https://appdevchallenge.auto-hmg.io/faq)
- [Pleos 첫 프로젝트](https://document.pleos.ai/en/docs/pleos-only/getting-started)
- [SDK 접근 상태](https://document.pleos.ai/en/docs/pleos-only/create-my-project)
- [에뮬레이터 환경](https://document.pleos.ai/en/docs/connect/guide/getting-started/application-development/setup-connect-sdk-emulator)

## 개발 시 확인
공식 안내의 SDK 이름과 실제 프로젝트 권한·artifact 다운로드 성공은 별개의 확인 항목이다.
사용 기능마다 API, 권한, 제공 상태, 에뮬레이터 결과, 미지원 시 동작을 기록한다.

- 공개 문서는 Vehicle State/NaviHelper를 Ready to Use로 안내한다.
- FusedLocation/TTS/STT/Vehicle Control은 공개 접근 안내에서 Not Available Yet로 표시될 수 있다. 개발 착수 시 다시 확인한다.
- 초기 조회에서 문서의 Vehicle:2.3.1 Maven POM은 404였다. 실제 연동이 완료됐다고 간주하지 않는다.
- mock 빌드는 개발·테스트용이다. 실제 차량 데이터 사용과 구분한다.
- Pleos SDK·에뮬레이터·Android API의 버전 숫자는 서로 다른 구성요소다.
- 운전 중 UI 제한, 미지원 기능, 권한 거부, 서비스 연결 종료와 네트워크 단절을 기능별로 검증한다.

제출 APK는 확인된 소스 SHA와 함께 제공한다. 공모전 제출과 마켓 정식 심사는 별도 완료 조건이다.
