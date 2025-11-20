# ==========================
# 1️⃣ 라이브러리 불러오기
# ==========================
import requests
import pandas as pd
import streamlit as st

# ==========================
# 2️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://openapi.gg.go.kr/GgWelfareCenter"

params = {
    "KEY": API_KEY,
    "Type": "xml",  # 요청 포맷은 XML
    "pIndex": 1,
    "pSize": 100
}

# ==========================
# 3️⃣ API 요청 및 데이터 가져오기
# ==========================
response = requests.get(BASE_URL, params=params)
if response.status_code != 200:
    st.error(f"❌ API 요청 실패: {response.status_code}")
else:
    try:
        # XML → DataFrame 변환
        df = pd.read_xml(response.content, xpath=".//row")
        
        # 컬럼 이름을 한글로 바꾸기
        rename_dict = {
            "BIZPLC_NM": "복지관명",
            "REFINE_ROADNM_ADDR": "도로명주소",
            "REFINE_LOTNO_ADDR": "지번주소",
            "TEL_NO": "전화번호",
            "INSTT_TYPE_NM": "복지관유형",
            "INSTT_STAT_NM": "운영상태"
        }
        df = df.rename(columns=rename_dict)
    except Exception as e:
        st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
        df = pd.DataFrame()

# ==========================
# 4️⃣ Streamlit 웹페이지 구성
# ==========================
st.title("경기도 장애인 복지관 현황 (자동 업데이트)")
st.write("✅ 최신 데이터를 바로 확인할 수 있습니다.")

if not df.empty:
    # 전체 표 보기
    st.subheader("전체 복지관 데이터")
    st.dataframe(df)

    # 복지관 이름 검색 기능
    st.subheader("복지관 검색")
    keyword = st.text_input("복지관 이름 입력")
    if keyword:
        filtered = df[df["복지관명"].str.contains(keyword)]
        if not filtered.empty:
            st.dataframe(filtered)
        else:
            st.write("해당 이름의 복지관이 없습니다.")
