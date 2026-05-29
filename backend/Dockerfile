# 1. 마이크로소프트의 Playwright 공식 이미지 사용 (우분투 기반, 브라우저 완비)
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 파이썬 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# (주의: 공식 이미지는 브라우저가 이미 깔려있어서 playwright install 명령어가 필요 없습니다!)

# 4. 나머지 소스코드 복사
COPY . .

# 5. 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
