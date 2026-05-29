import time
import random
from database import SessionLocal
from models import db_models

def validate_pending_orders():
    """DB에서 'pending(대기)' 상태인 주문을 찾아 통관부호를 검증합니다."""
    db = SessionLocal()
    try:
        # 1. 대기 중인 주문만 싹 필터링해서 가져오기
        pending_orders = db.query(db_models.Order).filter(db_models.Order.status == "pending").all()
        
        if not pending_orders:
            return # 검증할 주문이 없으면 그냥 종료

        print(f"🔍 [검증 엔진 가동] {len(pending_orders)}건의 대기 주문을 검사합니다...")

        for order in pending_orders:
            # 관세청 통신에 1초 정도 걸린다고 가정 (실제 딜레이 모방)
            time.sleep(1)
            
            # 임시 로직: 80% 확률로 정상 통과, 20% 확률로 이름/통관부호 불일치 에러 발생
            is_valid = random.random() > 0.2
            
            if is_valid:
                order.status = "processing" 
                # 이름 앞에 주문번호(order_id) 추가
                print(f"✅ [검증 성공] {order.order_id} ({order.customer_name})님의 통관부호 확인 완료. (상태: processing)")
            else:
                order.status = "error"      
                # 이름 앞에 주문번호(order_id) 추가
                print(f"❌ [검증 실패] {order.order_id} ({order.customer_name})님의 통관부호 불일치! 보류함으로 이동. (상태: error)")

        # 2. 변경된 상태값들을 DB에 최종 저장(도장 쾅)
        db.commit()

    except Exception as e:
        print(f"⚠️ 검증 엔진 에러 발생: {e}")
    finally:
        db.close()
