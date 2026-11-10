# 공모전과 Pleos 확인 사항

프로젝트는 Pleos Connect에서 실행할 Android 앱이다. 웹 UI가 필요하면 별도 저장소를 검토한다.

## 공식 자료
- [공모전 공고](https://appdevchallenge.auto-hmg.io/notice/c0a1a000-2026-4923-8000-000000000001)
- [공모전 FAQ](https://appdevchallenge.auto-hmg.io/faq)
- [Pleos 첫 프로젝트](https://document.pleos.ai/en/docs/pleos-only/getting-started)
- [SDK 접근 상태](https://document.pleos.ai/en/docs/pleos-only/create-my-project)
- [Vehicle SDK 가져오기](https://document.pleos.ai/en/docs/pleos-only/connect-sdk-pleos/Vehicle/project-setup)
- [Vehicle Maven 메타데이터](https://nexus-playground.pleos.ai/repository/maven-releases/ai/pleos/playground/Vehicle/maven-metadata.xml)
- [공식 Vehicle 예제](https://github.com/Pleos-Playground/pleos-sample-vehicle-app)
- [에뮬레이터 환경](https://document.pleos.ai/en/docs/connect/guide/getting-started/application-development/setup-connect-sdk-emulator)

## SDK 버전과 접근 확인

2026-11-10에 공개 Maven 저장소에서 `ai.pleos.playground:Vehicle:2.3.2`의 POM·AAR 다운로드를 확인했다.
빠른 시작 문서의 `2.3.1`은 POM 404지만, 가져오기 문서·공식 예제와 Maven 메타데이터의 `2.3.2`는 다운로드된다.
이전 404만으로 계정 권한 문제라고 판단하지 않는다. 현재 HPC-fe는 `2.3.2`를 고정한다.

- Maven 저장소: `https://nexus-playground.pleos.ai/repository/maven-releases/`
- AAR SHA-256: `e11fdfe498cad3ecc0d5a2a6992b0c4a4d135195f1455018127bc069fd5ef937`
- 위 값은 공식 `.aar.sha256` 및 Gradle module 메타데이터와 대조했다.
- artifact 다운로드, APK 빌드, 앱 실행, Vehicle Service 데이터 수신은 각각 별도로 검증한다.
- 공개 다운로드 가능 여부가 모든 SDK 기능·권한 또는 실차 사용 권한을 보장하지 않는다.

## 팀원의 에뮬레이터 준비

Android Studio의 SDK Manager → SDK Update Sites에 공식 Pleos 이미지 사이트를 추가한다.

- Windows/Linux: `https://nexus-playground.pleos.ai/repository/raw-releases/connect-avd/2.x/crp-sys-img.xml`
- Apple Silicon: `https://nexus-playground.pleos.ai/repository/raw-releases/connect-avd/2.x/crp-arm64-sys-img.xml`

SDK Platforms에서 **Show Package Details**를 켜고 Android API 34의 Pleos Connect 이미지를 설치한다.
Android Studio를 재시작한 뒤 Device Manager에서 Automotive → Pleos Connect v2.1.0 장치를 만들고,
API 34 / Pleos Connect v2.1.0 APIs 이미지, RAM 4 GB, Cold boot를 선택한다.
Windows/Linux x86_64 이미지 다운로드는 약 4.1 GB이며 압축 해제와 AVD 데이터용 여유 공간도 필요하다.
정확한 최신 설치 화면과 요구 사항은 위 공식 에뮬레이터 안내를 따른다.

Pleos는 [Quick boot에서 VHAL을 사용할 수 없음](https://document.pleos.ai/en/docs/connect/guide/getting-started/application-development/configure-pleos-connect-emulator)을 안내하므로 Cold boot를 유지한다.
headless 실행으로 부팅·앱 실행·SDK 조회를 확인할 수 있지만,
[Form Factor 멀티디스플레이 검사](https://document.pleos.ai/en/docs/pleos-only/app-test-guide/form-factor-test-guide)는 별도 에뮬레이터 창이 필요하다.
SDK 스모크 테스트 통과를 화면·주행 제한·실차 검증 완료로 확대 해석하지 않는다.

이후 APK 빌드·설치와 읽기 전용 SDK 스모크 테스트는 [HPC-fe README](https://github.com/Hyundai-Pleos-Contest/HPC-fe#readme)를 따른다.
`mock` 빌드는 일반 개발용이고, 실제 SDK 검사는 `-PenablePleos=true`와 전용 Pleos AVD를 사용한다.
Docker는 DB·BE·AI 실행에 사용하며 Android 앱은 에뮬레이터에서 실행한다.
BE 포트를 변경했다면 [Docker 빠른 시작](local-testing.md)의 Android 주소 설정도 함께 변경한다.

## 개발 시 확인
공식 안내의 SDK 이름과 실제 프로젝트 권한·artifact 다운로드 성공은 별개의 확인 항목이다.
사용 기능마다 API, 권한, 제공 상태, 에뮬레이터 결과, 미지원 시 동작을 기록한다.

- 공개 문서는 Vehicle State/NaviHelper를 Ready to Use로 안내한다.
- FusedLocation/TTS/STT/Vehicle Control은 공개 접근 안내에서 Not Available Yet로 표시될 수 있다. 개발 착수 시 다시 확인한다.
- mock 빌드는 개발·테스트용이다. 실제 차량 데이터 사용과 구분한다.
- Pleos SDK·에뮬레이터·Android API의 버전 숫자는 서로 다른 구성요소다.
- 운전 중 UI 제한, 미지원 기능, 권한 거부, 서비스 연결 종료와 네트워크 단절을 기능별로 검증한다.

제출 APK는 확인된 소스 SHA와 함께 제공한다. 공모전 제출과 마켓 정식 심사는 별도 완료 조건이다.
