# 가볍고 빠른 Python 3.11 환경 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 필수 패키지 설치 (Playwright 의존성 대비)
RUN apt-get update && apt-get install -y wget gnupg && rm -rf /var/lib/apt/lists/*

# 파이썬 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright용 가상 브라우저 설치 (가장 중요★)
RUN playwright install --with-deps chromium

# 나머지 백엔드 소스코드 전체 복사
COPY . .

# 서버 실행 명령어 (코드 수정 시 자동 재시작되는 --reload 옵션 켬)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
