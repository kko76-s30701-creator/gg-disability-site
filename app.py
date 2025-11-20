# ==========================
# 1️⃣ 라이브러리 불러오기
# ==========================
import requests
import pandas as pd
import streamlit as st
from xml.etree import ElementTree as ET


# ==========================
# 2️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://ggapi.gg.go.kr/Ggbizptinfo"

params = {
    "KEY": API_KEY,
    "Type": "xml",
    "pIndex": 1,
    "pSize": 1000  # 한 번에 최대 데이터 가져오기
}

# ==========================
# 3️⃣ API 요청 및 XML 파싱
# ==========================
response = requests.get(BASE_URL, params=params)
if response.status_code != 200:
    st.error(f"❌ API 요청 실패: {response.status_code}")
    df = pd.DataFrame()
else:
    try:
        root = ET.fromstring(response.content)
        items = []
        for row in root.findall(".//row"):
            items.append({
                "복지관명": row.findtext("BIZPLC_NM"),
                "주소": row.findtext("SITEWHL_ADDR"),
                "전화번호": row.findtext("TELNO"),
                "시설구분": row.findtext("FCLTY_DIV_NM"),
                "운영상태": row.findtext("OPST_STATE_NM")
            })
        df = pd.DataFrame(items)
    except Exception as e:
        st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
        df = pd.DataFrame()

# ==========================
# 4️⃣ Streamlit 웹페이지 구성
# ==========================
st.title("경기도 장애인 복지관 현황 (자동 업데이트)")
st.write("✅ 최신 데이터를 실시간으로 확인할 수 있습니다.")

if not df.empty:
    st.subheader("전체 복지관 데이터")
    st.dataframe(df)

    st.subheader("복지관 검색")
    search_name = st.text_input("복지관명으로 검색")
    if search_name:
        filtered = df[df["복지관명"].str.contains(search_name)]
        st.dataframe(filtered)
        st.text(response.text[:1000])  # 처음 1000글자만 출력


