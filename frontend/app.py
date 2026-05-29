import streamlit as st
import requests
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="Seller OS", page_icon="📦", layout="wide")

st.title("📦 Seller OS 자동화 대시보드")
st.markdown("백엔드 엔진과 RPA 봇이 실시간으로 처리 중인 주문 현황입니다.")

# 백엔드 API 주소 (로컬 호스트의 8000번 포트)
API_URL = "http://127.0.0.1:8000/api/orders"

def fetch_orders():
    """백엔드 엔진에서 실시간 주문 데이터를 긁어옵니다."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"백엔드 서버와 연결할 수 없습니다: {e}")
        return []

# 데이터 불러오기
orders = fetch_orders()

if orders:
    # JSON 데이터를 Pandas 표(DataFrame)로 변환
    df = pd.DataFrame(orders)
    
    # 상단 요약 지표 (Metrics) 보여주기
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 수집된 주문", f"{len(df)} 건")
    col2.metric("🟢 완료됨 (RPA 성공)", f"{len(df[df['status'] == 'completed'])} 건")
    col3.metric("🟡 처리 대기 중", f"{len(df[df['status'] == 'processing'])} 건")
    col4.metric("🔴 검증 오류 (보류)", f"{len(df[df['status'] == 'error'])} 건")
    
    st.divider()
    
    # 상태별로 색상을 다르게 보여주는 함수
    def color_status(val):
        color = 'green' if val == 'completed' else 'orange' if val == 'processing' else 'red' if val == 'error' else 'gray'
        return f'color: {color}; font-weight: bold;'
    
    # 예쁜 표로 데이터 출력
    st.subheader("📋 실시간 주문 처리 내역")
    st.dataframe(
        df.style.map(color_status, subset=['status']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("아직 수집된 주문 데이터가 없거나 서버가 꺼져있습니다.")

# 수동 새로고침 버튼
if st.button("🔄 실시간 데이터 새로고침"):
    st.rerun()
