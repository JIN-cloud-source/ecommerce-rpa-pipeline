import asyncio
from fastapi import FastAPI, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from services import market_api, validator, rpa_engine

from database import engine, get_db
from models import db_models, schemas
from services import market_api  # 🚀 가짜 마켓 서비스 불러오기

# DB 테이블 생성
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Seller OS Core API", version="1.0.0")

async def start_market_polling_scheduler():
    print("⏰ 수집 ➡️ 검증 ➡️ RPA 통합 스케줄러가 백그라운드에서 가동되었습니다.")
    while True:
        # Step 1. 마켓 주문 수집 (pending)
        await run_in_threadpool(market_api.fetch_and_save_mock_orders)
        
        # Step 2. 통관 부호 검증 (pending -> processing 또는 error)
        await run_in_threadpool(validator.validate_pending_orders)
        
        # Step 3. 대망의 RPA 봇 출동! (processing -> completed)
        await run_in_threadpool(rpa_engine.run_shipping_agent_rpa)
        
        await asyncio.sleep(10) # 10초 대기


# 🚀 FastAPI 서버가 시작될 때 스케줄러를 백그라운드 태스크로 등록
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_market_polling_scheduler())

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Backend engine is running smoothly!"}

# 주문 조회 API
@app.get("/api/orders", response_model=list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(db_models.Order).all()
    return orders
