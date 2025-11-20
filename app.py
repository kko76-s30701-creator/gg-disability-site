import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(page_title="경기도 장애인 복지관 현황", layout="wide")

st.title("경기도 장애인 복지관 현황 🌟")
st.markdown("경기도 내 장애인 복지관 정보를 확인하고, 검색할 수 있습니다.")

# ==========================
# 1️⃣ API 호출
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
URL = f"https://openapi.gg.go.kr/DisablePersonCmwelfct?KEY={API_KEY}&Type=xml&pIndex=1&pSize=1000"

try:
    response = requests.get(URL)
    response.raise_for_status()
except Exception as e:
    st.error(f"API 호출 실패: {e}")
    st.stop()

# ==========================
# 2️⃣ XML 파싱
# ==========================
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")
except Exception as e:
    st.error(f"XML 파싱 오류: {e}")
    st.stop()

# ==========================
# 3️⃣ 데이터프레임 생성
# ==========================
data = []
for r in rows:
    row_dict = {
        "기관명": r.findtext("BIZPLC_NM", default=""),
        "주소": r.findtext("REFINE_ROADNM_ADDR", default=""),
        "전화번호": r.findtext("ORG_TELNO", default=""),
        "대표자명": r.findtext("ORG_RPRSNTV_NM", default=""),
        "설립일": r.findtext("ESTB_DE", default=""),
        "운영기관": r.findtext("OPERT_INSTT_NM", default="")
    }
    data.append(row_dict)

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# ==========================
# 4️⃣ 검색 기능
# ==========================
search = st.text_input("복지관 이름 검색")
if search:
    filtered_df = df[df["기관명"].str.contains(search, case=False, na=False)]
else:
    filtered_df = df

st.write(f"총 {len(filtered_df)}개 기관이 검색되었습니다.")

# ==========================
# 5️⃣ 테이블 표시
# ==========================
st.dataframe(filtered_df.reset_index(drop=True))
