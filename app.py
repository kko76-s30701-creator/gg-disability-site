# ==========================
# 1️⃣ 라이브러리 불러오기
# ==========================
import requests
import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET

# ==========================
# 2️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://openapi.gg.go.kr/Ggregistdspsntypeage"

params = {
    "KEY": API_KEY,
    "Type": "xml",
    "pIndex": 1,
    "pSize": 100
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
        # XML 구조에 맞춰 'row' 요소 찾아서 리스트로 변환
        for row in root.findall(".//row"):
            item = {}
            for child in row:
                item[child.tag] = child.text
            items.append(item)
        df = pd.DataFrame(items)
    except Exception as e:
        st.error(f"⚠️ XML 파싱 실패: {e}")
        df = pd.DataFrame()

# ==========================
# 4️⃣ Streamlit 웹페이지 구성
# ==========================
st.title("경기도 장애인 복지관 현황 (자동 업데이트)")

st.write("✅ 최신 데이터가 자동으로 표시됩니다.")

if not df.empty:
    # 전체 데이터 보기
    st.subheader("전체 데이터")
    st.dataframe(df)

    # 사업장 이름 기준 검색
    st.subheader("사업장 이름 검색")
    search_name = st.text_input("검색어 입력 (사업장 이름)")
    if search_name:
        filtered = df[df["BIZPLC_NM"].str.contains(search_name, na=False)]
        st.dataframe(filtered)
        # ==========================
# 1️⃣ 라이브러리 불러오기
# ==========================
import requests
import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET

# ==========================
# 2️⃣ API 설정
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
BASE_URL = "https://ggapi.gg.go.kr/Ggbzplc"

params = {
    "KEY": API_KEY,
    "Type": "xml",
    "pIndex": 1,
    "pSize": 1000  # 충분히 많이 가져오기
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
        rows = []
        for item in root.findall(".//row"):
            rows.append({
                "복지관명": item.findtext("BIZPLC_NM"),
                "시군구": item.findtext("SIGUNGU_NM"),
                "주소": item.findtext("REFINE_ROADNM_ADDR"),
                "전화번호": item.findtext("TELNO"),
                "서비스": item.findtext("SERVC_TYPE")
            })
        df = pd.DataFrame(rows)
    except Exception as e:
        st.error(f"⚠️ 데이터 처리 오류: {e}")
        df = pd.DataFrame()

# ==========================
# 4️⃣ Streamlit 웹페이지 구성
# ==========================
st.title("경기도 장애인 복지관 현황")
st.write("✅ 최신 데이터가 자동으로 표시됩니다.")

if not df.empty:
    # 시군구 선택
    sigungu = st.selectbox("시군구 선택", sorted(df["시군구"].dropna().unique()))
    filtered = df[df["시군구"] == sigungu]

    # 서비스 선택 (다중)
    service_options = sorted(df["서비스"].dropna().unique())
    services = st.multiselect("서비스 종류 선택", service_options)
    if services:
        filtered = filtered[filtered["서비스"].isin(services)]

    # 테이블 표시
    st.dataframe(filtered.reset_index(drop=True))
else:
    st.write("데이터가 없습니다.")

