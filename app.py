# ==========================
# 0️⃣ 라이브러리 설치
# ==========================
!pip install streamlit pandas requests lxml

# ==========================
# 1️⃣ 라이브러리 불러오기
# ==========================
import requests
import pandas as pd
import streamlit as st
from io import BytesIO
import xml.etree.ElementTree as ET

# ==========================
# 2️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://ggapi.gg.go.kr/AssistDsgnBizInfo"
params = {
    "KEY": API_KEY,
    "Type": "xml",
    "pIndex": "1",
    "pSize": "100"
}

# ==========================
# 3️⃣ API 요청 및 XML 파싱
# ==========================
response = requests.get(BASE_URL, params=params)
if response.status_code != 200:
    st.error(f"❌ API 요청 실패: {response.status_code}")
else:
    try:
        root = ET.fromstring(response.content)
        items = []
        for row in root.findall(".//row"):
            item = {child.tag: child.text for child in row}
            items.append(item)
        df = pd.DataFrame(items)
    except Exception as e:
        st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
        df = pd.DataFrame()

# ==========================
# 4️⃣ 컬럼 한글명 변경
# ==========================
if not df.empty:
    df = df.rename(columns={
        "BIZPLC_NM": "복지관명",
        "ADDR": "주소",
        "TELNO": "전화번호",
        "RPRSNTV_NM": "대표자",
        "INSTT_TYPE_NM": "기관유형",
        "OPEN_DATE": "개설일",
        "BIZCND_TYPE_NM": "사업현황"
    })

# ==========================
# 5️⃣ Streamlit 웹페이지 구성
# ==========================
st.title("경기도 장애인 복지관 현황 (자동 업데이트)")

st.write("✅ 최신 데이터를 확인할 수 있습니다.")

if not df.empty:
    # 전체 표 보기
    st.subheader("전체 복지관 데이터")
    st.dataframe(df)

    # 복지관 이름 검색
    st.subheader("복지관 이름으로 검색")
    keyword = st.text_input("복지관 이름 입력")
    if keyword:
        filtered = df[df["복지관명"].str.contains(keyword)]
        st.dataframe(filtered)
