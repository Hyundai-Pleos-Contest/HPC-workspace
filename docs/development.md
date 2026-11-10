# 개발 환경과 실행

## 도구와 경로
- Git, Docker Desktop(Linux engine), Compose를 준비한다.
- Android는 HPC-fe에 고정된 JDK/Gradle/SDK 조합과 Android Studio를 사용한다.
- BE는 JDK 21, AI는 Python 3.12와 uv를 사용한다.
- workspace 검사 스크립트는 Python 3.12 이상 표준 라이브러리만 사용한다.
- Gradle Wrapper와 uv.lock을 사용한다. 시스템 전역 Gradle이나 임의 pip 설치에 의존하지 않는다.
- 네 저장소를 형제 폴더로 배치한다. 개별 저장소 실행에는 형제 폴더가 필수가 아니며 통합 Compose 빌드에만 BE/AI 경로가 필요하다.

## Compose
[Docker 로컬 테스트 빠른 시작](local-testing.md)에 운영체제별 설정 복사, 실행 범위 선택,
health 확인, 포트 충돌 대응, 재빌드와 DB를 보존하는 종료 명령을 모았다.
Compose는 HPC-workspace의 `.env`를 변수 치환에 사용한다. 실제 주입 항목은 `compose.yaml`의 `environment`가 기준이다.
이 Compose는 개발 전용으로 호스트 포트를 loopback에 바인딩한다. 실제 배포·TLS·인증은 후속 작업이다.

## 환경 변수
- POSTGRES_DB/POSTGRES_USER/POSTGRES_PASSWORD: 개발 DB 설정. 예제 비밀번호를 외부 환경에 재사용하지 않는다.
- POSTGRES_PORT/BE_PORT/AI_PORT: 호스트 포트. 컨테이너 포트는 각각 5432/8080/8000이다.
- IDE에서 BE를 직접 실행할 때는 HPC-be 안내에 따라 환경변수를 주입한다. Spring Boot가 .env를 자동 읽는다고 가정하지 않는다.
- AI의 직접 실행 설정은 HPC-ai README가 원본이다.
- Android의 서버 주소는 HPC-fe Gradle 설정을 따른다. .env나 비밀키를 APK에 포함하지 않는다.

## 확인
[빠른 시작](local-testing.md)의 상태 확인과 Android 주소 설정 절차를 따른다.
BE_PORT를 바꾸었다면 호스트 확인 URL과 앱의 개발 주소도 함께 바꾼다. 실기기는 별도 HTTPS 연결 경로가 필요하다.

## 통합 범위
현재 BE와 AI는 각각 기본 상태 확인만 제공한다. AI_BASE_URL 설정은 향후 연결 지점이며,
BE가 AI를 호출하는 기능이 구현됐다는 의미가 아니다.
Pleos 에뮬레이터와 실제 Vehicle SDK 연동 확인은 일반 Android 빌드와 별도로 기록한다.
