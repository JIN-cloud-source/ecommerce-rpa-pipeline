from fastapi import FastAPI

# FastAPI 앱 초기화
app = FastAPI(title="Seller OS Core API", version="1.0.0")

@app.get("/")
def read_root():
    """서버가 정상적으로 켜졌는지 확인하는 헬스 체크용 API"""
        return {"status": "ok", "message": "Backend engine is running smoothly!"}

        @app.get("/api/orders/test")
        def test_order_fetch():
            """프론트엔드 연동 테스트를 위한 더미 데이터"""
                return {
                        "orders": [
                                    {"customer_name": "홍길동", "address": "서울특별시 강남구", "pccc": "P123456789012"},
                                                {"customer_name": "김철수", "address": "경기도 남양주시", "pccc": "P098765432109"}
                                                        ]
                                                            }
                                                            