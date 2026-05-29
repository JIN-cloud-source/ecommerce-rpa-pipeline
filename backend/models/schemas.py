from pydantic import BaseModel

# 공통적으로 사용할 주문 데이터 형식
class OrderBase(BaseModel):
    order_id: str
    customer_name: str
    address: str
    pccc: str

# 새로운 주문을 DB에 생성할 때 사용할 형식 (입력용)
class OrderCreate(OrderBase):
    pass

# DB에서 데이터를 꺼내서 프론트엔드에 응답할 때 사용할 형식 (출력용)
class OrderResponse(OrderBase):
    id: int
    status: str

    class Config:
        from_attributes = True # SQLAlchemy DB 모델을 Pydantic 모델로 자동 변환해 주는 마법의 옵션
