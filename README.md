# FastAPI 세미나 과제 1

세미나 1에서 FastAPI 의 기본적인 사용법을 익혔지만, 본 과제에서는 여러분이 배우지 않은 내용이 나올 수 있습니다.
아무리 똑똑한 개발자라도 모든 것을 다 알 수는 없습니다.
그렇기에 검색을 통해 필요한 정보를 찾아내는 능력도 중요합니다.
과제를 수행하면서 모르는 부분이 있으면 검색을 통해 스스로 해결해보세요.
물론, #fastpi-잡담 채널에서 질문해도 좋습니다. 정답을 직접적으로 알려주지는 않겠지만, 방향을 잡아드릴 수 있습니다.

## 과제 목표

- HTTP 요청을 원하는 형태로 파싱할 수 있다.
- HTTP 응답을 원하는 형태로 생성할 수 있다.
- 클라이언트와 서버 에러를 구분하고, 적절하게 처리할 수 있다.

## 준비 사항

- 모든 과제는 python 3.11 버전을 사용할 것을 전제로 합니다.
- 본 과제부터 가상환경의 생성은 poetry 를 사용합니다.
  - poetry 를 설치한 뒤, `poetry env use -- 3.11` 과 같은 명령어를 이용해 가상환경을 생성하세요.
  - `poetry install` 명령어를 통해 패키지를 설치하세요.
  - `pyproject.toml` 과 `poetry.lock` 파일은 수정하지 않습니다.

## 과제 1-1

여러분은 로켓배송으로 유명한 와팡의 개발자입니다. 우선, 과제 1에서는 와팡의 회원가입 및 프로필 조회, 수정 API 를 구현해 봅시다.

### 회원가입 API

- 회원가입 API 는 POST 메서드로 `/api/user/signup` 엔드포인트에 요청을 보내야 합니다.
- 요청 본문은 JSON 형식으로, `username`, `password`, `email` 필드를 포함해야 합니다.
- `username` 필드는 3글자 이상 20글자 이하의 문자열이어야 합니다. 영문 대소문자, 숫자, `_`, `-` 만을 포함해야 합니다.
- `password` 필드는 8글자 이상 20글자 이하의 문자열이어야 합니다. 영문 대소문자, 숫자, 특수문자 중 2가지 이상을 포함해야 합니다.
- `email` 필드는 이메일 형식이어야 합니다.
- 회원가입에 성공하면 `201 Created` 상태코드를 반환합니다.
  - 회원가입에 성공한 유저 정보는 데이터베이스에 저장합니다.
  - 여러분들은 아직 데이터베이스를 다루는 방법을 배우지 않았기 때문에, 인메모리에 저장하는 방식으로 구현하면 됩니다.
  - 관련 코드는 `/wapang/app/user/models.py` 파일에 작성합니다.
- 회원가입에 실패하는 경우는 다음과 같습니다.
  - `username`, `password`, `email` 필드 중 하나라도 없는 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Missing required fields"}`
  - `username`, `password`, `email` 필드의 제한 사항, 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 이미 존재하는 `username` 또는 `email` 필드를 사용하는 경우
    - `409 Conflict` 상태코드와 함께 응답으로 `{"detail": "Username already exists"}` 또는 `{"detail": "Email already exists"}`

### 프로필 조회 API

- 프로필 조회 API 는 GET 메서드로 `/api/user/me` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 회원가입된 유저의 경우, `200 OK` 상태코드와 함께 `username`, `email`, `address`, `phone_number` 필드를 포함한 JSON 응답을 반환합니다.
  - 이제 막 회원가입한 유저의 경우 `address`, `phone_number` 필드는 `null` 로 반환합니다.
- 회원가입되지 않은 유저의 경우, `401 Unauthorized` 상태코드를 반환합니다.

### 프로필 수정 API

- 프로필 수정 API 는 PATCH 메서드로 `/api/user/me` 엔드포인트에 요청을 보내야 합니다.
- 요청 헤더에는 `X-Wapang-Username`, `X-Wapang-Password` 필드를 포함해야 합니다.
- 요청 본문은 JSON 형식으로, `email`, `address`, `phone_number` 필드를 포함할 수 있습니다.
- `email` 필드는 이메일 형식이어야 합니다.
- `address` 필드는 100글자 이하의 문자열이어야 합니다.
- `phone_number` 필드는 010으로 시작하는 11자리 숫자형식 문자열이어야 합니다.
- 프로필 수정에 성공하면 `200 OK` 상태코드를 반환합니다.
- 프로필 수정에 실패하는 경우는 다음과 같습니다.
  - `email`, `address`, `phone_number` 필드 중 하나라도 형식이 올바르지 않은 경우
    - `400 Bad Request` 상태코드와 함께 응답으로 `{"detail": "Invalid field format"}`
  - 회원가입되지 않은 유저의 경우
    - `401 Unauthorized` 상태코드를 반환합니다.
  - 이미 존재하는 `email` 필드를 사용하는 경우
    - `409 Conflict` 상태코드와 함께 응답으로 `{"detail": "Email already exists"}`


## 과제 1-2

이제 여러분들이 구현한 API 를 EC2 인스턴스에 배포해보겠습니다.

### EC2 인스턴스 생성

- #fastapi-공지 채널에서 공지한 특별 과제로 대체합니다.

### API 서버 배포

- EC2 인스턴스에 접속하여, 과제 레포지터리를 클론합니다.
- `poetry` 로 가상환경을 설정하고, `uvicorn` 으로 FastAPI 서버를 실행합니다. 이 때 외부 접속을 허용하기 위해, `--host 0.0.0.0` 옵션을 사용합니다.
- 사용자는 1024번 이하 포트를 사용할 권한이 없으므로, `--port 8000` 과 같은 옵션을 사용하여 포트를 지정합니다.
  - 대신 외부에서 80번 포트로 접속할 수 있도록 추가적인 설정을 해야 합니다.
  - 세미나에서는 sudo 권한으로 `uvicorn` 을 80 번 포트로 실행했지만, 이 방법은 보안 상 취약하므로 사용하지 않습니다.
  - 대신, Nginx 와 같은 웹 서버로 리버스 프록시를 설정하거나, 포트 포워딩을 사용합니다.
  - 이번 과제에서는 웹 서버를 사용하지 않고 해결해보겠습니다. (hint: `iptables`)
- 셸에서 로그아웃하더라도 서버가 계속 실행되어야 합니다. 어떻게 하면 좋을지 한 번 찾아보세요!

## 채점 기준

- 모든 API 가 요구사항에 맞게 동작하는가?
- 요구사항에 맞게 적절한 상태코드와 응답을 반환하는가?
- 타입 힌트를 적절하게 사용하였는가?
- 4xx 에러를 처리하기 위해 적절한 exception_handler 를 사용하였는가?
- EC2 인스턴스에 API 서버를 성공적으로 배포하였는가?
- EC2 인스턴스에서 서버가 24시간 실행되도록 설정하였는가?
- EC2 인스턴스의 80번 포트로 접속하여 API 서버가 정상적으로 동작하는가?

## 제출 방법

과제 수락 시 생성된 레포지터리의 `main` 브랜치에 완성된 코드를 푸시하세요.

**(주의⚠️) Feedback PR 은 머지하지 마세요!**

## 참고 문서

- [세미나1 강의자료](https://minkyu97.github.io/fastapi-seminar-presentation/decks/seminar1/)
- [FastAPI 공식 튜토리얼](https://fastapi.tiangolo.com/tutorial/)
- [iptables man page](https://manpages.ubuntu.com/manpages/noble/en/man8/iptables.8.html)
