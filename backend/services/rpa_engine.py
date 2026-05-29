import time
from playwright.sync_api import sync_playwright
from database import SessionLocal
from models import db_models

def run_shipping_agent_rpa():
    """DB에서 검증 완료된 주문을 가져와 실제 폼 입력을 진행합니다."""
    db = SessionLocal()
    try:
        # 1. 검증 완료(processing) 상태인 주문 하나 가져오기
        target_order = db.query(db_models.Order).filter(db_models.Order.status == "processing").first()
        if not target_order:
            return

        print(f"🤖 [RPA 봇 출동] 주문번호 {target_order.order_id} ({target_order.customer_name})님의 봇 작업 시작.")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print("🌐 로그인 폼 페이지 접속 중...")
            page.goto("https://practicetestautomation.com/practice-test-login/")
            
            # ==========================================
            # 防어막 1: 명시적 대기 (Explicit Wait)
            # ==========================================
            # 페이지가 열렸어도 입력창 엘리먼트가 화면에 완전히 나타날(visible) 때까지 최대 5초간 안전하게 기다립니다.
            # 서버 컨디션이 나빠서 로딩이 2~3초 걸려도 봇이 뻗지 않고 유연하게 버팁니다.
            username_input = page.locator("input#username")
            username_input.wait_for(state="visible", timeout=5000)
            
            # ==========================================
            # 防어막 2: 기습 팝업창 제어 (Popup Handling)
            # ==========================================
            # 실무 배대지 사이트에서 무작위로 뜨는 '오늘 하루 이 창 열지 않기' 레이어 팝업을 우회하는 로직입니다.
            # 팝업 닫기 버튼(예: button#close-popup)이 화면에 떴는지 0.5초만 살짝 체크하고, 있으면 부드럽게 닫고 지나갑니다.
            popup_close_button = page.locator("button#close-today-popup")
            if popup_close_button.is_visible(timeout=500): 
                popup_close_button.click()
                print("🧹 [팝업 차단] 화면을 가리고 있던 배너 팝업을 감지하여 안전하게 닫았습니다.")
            
            # 3. 로그인 진행
            print("⌨️ 아이디와 비밀번호를 타이핑합니다...")
            username_input.fill("student")
            time.sleep(1) # 봇 탐지 우회를 위한 사람 흉내 딜레이
            
            page.locator("input#password").fill("Password123")
            time.sleep(1)
            
            page.locator("button#submit").click()
            
            # 로그인 완료 후 다음 주소로 완전히 넘어갈 때까지 대기하는 명시적 대기 문법
            page.wait_for_url("**/logged-in-successfully/")
            
            # 4. 배송 정보 폼 데이터 입력 로직 (이전 단계 구조 유지)
            print(f"✍️ {target_order.customer_name}님의 배송 정보를 입력합니다...")
            time.sleep(1) 
            
            print("✅ 배송 정보 폼 타이핑 및 제출 완료!")
            
            # 5. 임무 완수 후 DB 상태 업데이트
            target_order.status = "completed"
            db.commit()
            
            print(f"🎉 [RPA 완료] {target_order.order_id} 자동 작성 성공! (상태: completed)")
            browser.close()

    except Exception as e:
        print(f"🚨 RPA 봇 구동 중 에러 발생: {e}")
        # 에러가 나면 해당 주문을 error 상태로 돌려놓아 대시보드에 빨간불이 켜지게 만듭니다.
        if 'target_order' in locals() and target_order:
            target_order.status = "error"
            db.commit()
    finally:
        db.close()
