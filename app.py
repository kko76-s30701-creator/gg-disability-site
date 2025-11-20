import requests
import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET

st.set_page_config(page_title="경기도 장애인 복지관 현황", layout="wide")
st.title("경기도 장애인 복지관 현황 (실시간 업데이트)")

# ==========================
# 1️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://ggapi.gg.go.kr/GgDisabilityWelfareFacility"

params = {
    "KEY": API_KEY,
    "Type": "xml",
    "pIndex": 1,
    "pSize": 1000
}

# ==========================
# 2️⃣ API 요청
# ==========================
try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
except Exception as e:
    st.error(f"❌ API 요청 실패: {e}")
    st.stop()

# ==========================
# 3️⃣ XML 파싱
# ==========================
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")

    data = []
    for r in rows:
        data.append({
            "복지관명": r.findtext("BIZPLC_NM", default=""),
            "주소": r.findtext("SITEWHL_ADDR", default=""),
            "전화번호": r.findtext("TELNO", default=""),
            "시설구분": r.findtext("FCLTY_SE", default=""),
            "운영상태": r.findtext("OP_STTUS", default="")
        })

    df = pd.DataFrame(data)

    if df.empty:
        st.warning("⚠️ 데이터가 없습니다.")
    else:
        st.subheader("전체 복지관 현황")
        st.dataframe(df, use_container_width=True)

        st.subheader("복지관 검색")
        keyword = st.text_input("복지관 이름 입력 (부분 검색 가능)")
        if keyword:
            filtered = df[df["복지관명"].str.contains(keyword, na=False)]
            if filtered.empty:
                st.info("검색 결과가 없습니다.")
            else:
                st.dataframe(filtered, use_container_width=True)

except ET.ParseError:
    st.error("⚠️ XML 데이터 파싱 중 오류 발생")
except Exception as e:
    st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
