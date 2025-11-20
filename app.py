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
 # 3️⃣ 필요한 컬럼만 선택 및 한글명으로 변경
        # ==========================
        df = df[[
            "BSN_STATE_NM",
            "LOCPLC_AR",
            "ENTRNC_PSN_CAPA",
            "QUALFCTN_POSESN_PSN_CNT",
            "TOT_PSN_CNT"
        ]]
        df.rename(columns={
            "BSN_STATE_NM": "영업상태명",
            "LOCPLC_AR": "소재지면적(㎡)",
            "ENTRNC_PSN_CAPA": "입소정원(명)",
            "QUALFCTN_POSESN_PSN_CNT": "자격소유인원수(명)",
            "TOT_PSN_CNT": "총인원수(명)"
        }, inplace=True)
        
    except Exception as e:
        st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
        df = pd.DataFrame()


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
