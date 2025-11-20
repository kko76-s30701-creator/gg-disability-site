import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(page_title="경기도 장애인 복지관 현황", layout="wide")

st.title("가톨릭대 주변 장애인 복지관 🌟")
st.markdown("장애인 복지관 정보를 확인하고, 검색할 수 있습니다.")

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
data = []
for r in rows:
    row_dict = {
        "기관명": r.findtext("BIZPLC_NM", default=""),
        "주소": r.findtext("REFINE_ROADNM_ADDR", default=""),
        "영업상태명": r.findtext("BSN_STATE_NM", default=""),
        "소재지면적(㎡)": r.findtext("LOCPLC_AR", default=""),
        "입소정원(명)": r.findtext("ENTRNC_PSN_CAPA", default=""),
        "자격소유인원수(명)": r.findtext("QUALFCTN_POSESN_PSN_CNT", default=""),
        "총인원수(명)": r.findtext("TOT_PSN_CNT", default="")
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
