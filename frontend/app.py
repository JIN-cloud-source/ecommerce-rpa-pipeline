import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Seller OS", page_icon="📦", layout="wide")

st.title("📦 Seller OS 자동화 대시보드")
st.markdown("백엔드 엔진과 RPA 봇이 실시간으로 처리 중인 주문 현황입니다.")

API_URL = "http://127.0.0.1:8000/api/orders"

# ==========================================
# 📁 사이드바: 엑셀 & CSV 파일 업로드 영역
# ==========================================
st.sidebar.header("📥 신규 주문서 업로드")
st.sidebar.markdown("스마트스토어/쿠팡 엑셀 또는 CSV 파일을 올려주세요.")

# type에 'csv' 추가!
uploaded_file = st.sidebar.file_uploader("주문 파일 선택 (.xlsx, .csv)", type=['xlsx', 'csv'])

if uploaded_file:
    # 1. 파일 확장자에 따라 알맞은 엔진으로 읽기
    if uploaded_file.name.endswith('.csv'):
        df_new = pd.read_csv(uploaded_file) # CSV 읽기
    else:
        df_new = pd.read_excel(uploaded_file) # 엑셀 읽기
        
    st.sidebar.success(f"{len(df_new)}건의 데이터 로드 완료!")
    
    # 2. 미리보기 제공
    st.sidebar.markdown("**데이터 미리보기**")
    st.sidebar.dataframe(df_new.head(3), use_container_width=True)
    
    # 3. 백엔드로 데이터 쏘기 버튼
    if st.sidebar.button("🚀 DB로 전송 (자동화 시작)", use_container_width=True):
        success_count = 0
        for index, row in df_new.iterrows():
            payload = {
                "order_id": str(row.get("주문번호", f"EXCEL-{index}")),
                "customer_name": str(row.get("구매자명", "알수없음")),
                "address": str(row.get("배송지", "주소없음")),
                "pccc": str(row.get("통관번호", "P000000000000"))
            }
            res = requests.post(API_URL, json=payload)
            if res.status_code == 200:
                success_count += 1
                
        st.sidebar.success(f"총 {success_count}건 DB 전송 완료! 봇이 작업을 시작합니다.")

# ==========================================
# 📊 기존: 실시간 주문 처리 내역 조회 (이하 동일)
# ==========================================
def fetch_orders():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

orders = fetch_orders()

if orders:
    df = pd.DataFrame(orders)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 수집된 주문", f"{len(df)} 건")
    col2.metric("🟢 완료됨", f"{len(df[df['status'] == 'completed'])} 건")
    col3.metric("🟡 처리 대기 중", f"{len(df[df['status'] == 'processing'])} 건")
    col4.metric("🔴 검증 오류", f"{len(df[df['status'] == 'error'])} 건")
    
    st.divider()
    
    def color_status(val):
        color = 'green' if val == 'completed' else 'orange' if val == 'processing' else 'red' if val == 'error' else 'gray'
        return f'color: {color}; font-weight: bold;'
    
    st.subheader("📋 실시간 주문 처리 내역")
    st.dataframe(df.style.map(color_status, subset=['status']), use_container_width=True, hide_index=True)
else:
    st.info("아직 수집된 주문 데이터가 없거나 서버가 꺼져있습니다.")

if st.button("🔄 실시간 데이터 새로고침"):
    st.rerun()
