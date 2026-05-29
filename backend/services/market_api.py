import random
from database import SessionLocal
from models import db_models

def fetch_and_save_mock_orders():
    """오픈마켓 API를 찔러서 새 주문을 가져온 뒤 DB에 저장하는 과정을 흉내 냅니다."""
    db = SessionLocal()
    try:
        # 가짜 데이터 후보군
        names = ["이단비", "박민수", "최현우", "정수아", "강태호"]
        addresses = ["인천광역시 부평구 부평대로 10", "부산광역시 해운대구 수영강변대로 50", "대전광역시 서구 둔산로 20"]
        
        # 가짜 주문 1건 생성
        mock_id = random.randint(1000, 9999)
        mock_order = db_models.Order(
            order_id=f"MOCK-{mock_id}",
            customer_name=random.choice(names),
            address=random.choice(addresses),
            pccc=f"P{random.randint(100000000000, 999999999999)}"
        )
        
        db.add(mock_order)
        db.commit()
        print(f"📡 [마켓 수집 완료] 주문번호 {mock_order.order_id} ({mock_order.customer_name}) 데이터가 DB에 자동 동기화되었습니다.")
    except Exception as e:
        print(f"❌ 마켓 수집 중 에러 발생: {e}")
    finally:
        db.close()
