import requests
import pandas as pd
import streamlit as st

# -----------------------------
# 1) 기본 설정
# -----------------------------
st.title("경기도 장애인 복지관 현황")
st.write("이 앱은 경기도 공공데이터 API에서 정보를 받아와 실시간으로 업데이트됩니다.")

API_KEY = "c9955392cc82450eb32d33c996ad1a9a"   # 당신의 인증키
API_URL = f"https://openapi.gg.go.kr/OldPeopleCenter?KEY={API_KEY}&Type=json&pIndex=1&pSize=200"

# -----------------------------
# 2) API 요청
# -----------------------------
def load_data():
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error("API 요청 실패. 인증키 또는 URL을 확인하세요.")
        return None

    data = response.json()

    # JSON 구조 확인 후 실제 데이터 테이블 꺼내기
    try:
        rows = data["OldPeopleCenter"][1]["row"]
        df = pd.DataFrame(rows)
        return df
    except:
        st.error("API 데이터 구조가 예상과 다릅니다.")
        return None

# -----------------------------
# 3) 데이터 불러오기 및 표시
# -----------------------------
df = load_data()

if df is not None:
    st.success("데이터 불러오기 성공!")
    st.dataframe(df)

    # 검색 기능
    name = st.text_input("🔍 복지관 이름 검색")

    if name:
        filtered = df[df["BIZPLC_NM"].str.conta_]()]()
