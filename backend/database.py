from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite 데이터베이스 파일 생성 경로 (도커 컨테이너 내부)
SQLALCHEMY_DATABASE_URL = "sqlite:///./seller.db"

# DB 엔진 생성 (SQLite 특성상 쓰레드 설정 추가)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# DB에 접근하기 위한 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 앞으로 만들 모든 DB 모델의 부모 클래스
Base = declarative_base()

# DB 세션을 가져오고 반환하는 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
