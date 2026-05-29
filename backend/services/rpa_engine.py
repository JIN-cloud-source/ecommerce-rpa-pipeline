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
            
            # 2. 테스트용 로그인 웹사이트 접속
            print("🌐 로그인 폼 페이지 접속 중...")
            page.goto("https://practicetestautomation.com/practice-test-login/")
            
            # 3. 아이디 입력 (id가 'username'인 입력창을 찾아서 텍스트 채우기)
            print("⌨️ 아이디와 비밀번호를 타이핑합니다...")
            page.locator("input#username").fill("student")
            time.sleep(1) # 실무 팁: 봇 탐지를 피하기 위해 사람처럼 1초 쉬어주기
            
            # 4. 비밀번호 입력 (id가 'password'인 입력창 타겟팅)
            page.locator("input#password").fill("Password123")
            time.sleep(1)
            
            # 5. 로그인 버튼 클릭 (id가 'submit'인 버튼 타겟팅)
            print("🖱️ 로그인 버튼 클릭!")
            page.locator("button#submit").click()
            
            # 6. 로그인 성공 확인 (다음 페이지로 URL이 넘어갈 때까지 대기)
            page.wait_for_url("**/logged-in-successfully/")
            print(f"🔓 [로그인 성공!] 방화벽을 뚫고 내부에 진입했습니다. (현재 URL: {page.url})")
            
            # 7. 임무 완수 후 DB 상태 업데이트
            target_order.status = "completed"
            db.commit()
            
            print(f"🎉 [RPA 완료] {target_order.order_id} 자동 작성 성공! (상태: completed)")
            browser.close()

    except Exception as e:
        print(f"🚨 RPA 봇 구동 중 에러 발생: {e}")
        # 에러가 나면 해당 주문을 error 상태로 돌려놓음
        if 'target_order' in locals() and target_order:
            target_order.status = "error"
            db.commit()
    finally:
        db.close()
