from sqlalchemy import Column, Integer, String
from backend.database import Base

class Order(Base):
    __tablename__ = "orders" # DB에 생성될 실제 테이블 이름

    id = Column(Integer, primary_key=True, index=True) # 고유 번호
    order_id = Column(String, unique=True, index=True) # 오픈마켓 주문 번호
    customer_name = Column(String, index=True)         # 고객 이름
    address = Column(String)                           # 배송지 주소
    pccc = Column(String)                              # 개인통관고유부호 (PCCC)
    status = Column(String, default="pending")         # 현재 상태 (pending, processing, completed, error)
    