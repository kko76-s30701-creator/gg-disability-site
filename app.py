import requests
import pandas as pd
import streamlit as st

# ==========================
# 1️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://openapi.gg.go.kr/Ggregistdspsntypeage"

params = {
    "KEY": API_KEY,
    "Type": "json",
    "pIndex": 1,
    "pSize": 100  # 최대 100개
}

# ==========================
# 2️⃣ 데이터 가져오기
# ==========================
response = requests.get(BASE_URL, params=params)
if response.status_code != 200:
    st.error(f"❌ API 요청 실패: {response.status_code}")
    df = pd.DataFrame()
else:
    data = response.json()
    try:
        items = data["Ggregistdspsntypeage"][1]["row"]
        df = pd.DataFrame(items)
    except Exception as e:
        st.error("⚠️ 데이터 구조가 예상과 다릅니다.")
        df = pd.DataFrame()

# ==========================
# 3️⃣ Streamlit 앱 구성
# ==========================
st.title("경기도 장애인 복지관 현황")
st.write("✅ 최신 데이터가 자동으로 표시됩니다.")

if not df.empty:
    # 전체 데이터
    st.subheader("전체 데이터")
    st.dataframe(df)

    # 복지관 이름 검색
    st.subheader("복지관 이름으로 검색")
    search_name = st.text_input("복지관 이름 입력")
    if search_name:
        filtered = df[df["BIZPLC_NM"].str.contains(search_name)]
        st.dataframe(filtered)

    # 장애유형 선택
    st.subheader("장애유형별 검색")
    obstacle_type = st.selectbox("장애유형 선택", df['OBSTCL_TYPE'].unique())
    st.dataframe(df[df['OBSTCL_TYPE'] == obstacle_type])
