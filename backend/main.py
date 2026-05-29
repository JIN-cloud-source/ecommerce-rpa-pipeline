import asyncio
from fastapi import FastAPI, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from database import engine, get_db
from models import db_models, schemas
from services import validator, rpa_engine  # market_api(가짜수집기)는 이제 은퇴!

# DB 테이블 생성
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Seller OS Core API", version="1.0.0")

# 🕰️ 백그라운드 스케줄러 (가짜 생성은 빼고, 검증/RPA만 돕니다!)
async def start_rpa_scheduler():
    print("⏰ 통관 검증 및 RPA 봇 대기열 스케줄러 가동 중...")
    while True:
        # 가짜 주문 수집 로직 삭제! (이제 엑셀에서만 주문이 들어옵니다)
        
        # 1. 엑셀로 들어온 주문들 통관 번호 검증
        await run_in_threadpool(validator.validate_pending_orders)
        
        # 2. 통과된 주문들 RPA 봇 출동
        await run_in_threadpool(rpa_engine.run_shipping_agent_rpa)
        
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_rpa_scheduler())

# ==========================================
# 🌟 복구된 API 창구들
# ==========================================

# [신규] 엑셀에서 데이터를 받아 DB에 넣어주는 POST 라우터!
@app.post("/api/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db_models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# 기존 주문 목록 조회 API
@app.get("/api/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(db_models.Order).all()
    return orders
