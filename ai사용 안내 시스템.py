import streamlit as st

st.set_page_config(
    page_title="AI 사용 안내 시스템",
    page_icon="💡",
    layout="centered"
)

st.markdown("""
<style> 
html, body, [class*="css"] {
    font-size: 20px;
}
.stButton button {
    min-height: 50px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("💡 AI 사용 안내 시스템")
st.write("AI 사용이 어려우신가요? 필요한 도움을 선택해 보세요!")

st.info("누구나 쉽게 따라 할 수 있도록 단계별로 안내합니다.")

menu = st.selectbox(
    "어떤 도움이 필요하신가요?",
    [
        "AI에게 질문하기",
        "사진 올리기",
        "음성으로 질문하기",
        "답변이 이해되지 않아요",
        "AI 답변이 맞는지 확인하기"
    ]
)

guides = {
    "AI에게 질문하기": [
        "1. AI 서비스에 접속합니다.",
        "2. 질문을 입력하는 칸을 찾습니다.",
        "3. 궁금한 내용을 쉽고 구체적으로 적습니다.",
        "4. 보내기 버튼을 누릅니다.",
        "5. 답변을 읽고 모르는 부분은 다시 질문합니다."
    ],
    "사진 올리기": [
        "1. 질문 입력창 근처의 사진 또는 파일 첨부 버튼을 찾습니다.",
        "2. 기기에 저장된 사진을 선택합니다.",
        "3. 사진에 대해 궁금한 내용을 적습니다.",
        "4. 보내기 버튼을 누릅니다.",
        "5. AI가 알려 주는 설명을 확인합니다."
    ],
    "음성으로 질문하기": [
        "1. 마이크 또는 음성 대화 버튼을 찾습니다.",
        "2. 마이크 사용을 허용합니다.",
        "3. 버튼을 누르고 궁금한 내용을 말합니다.",
        "4. AI의 답변을 듣거나 화면에서 읽습니다."
    ],
    "답변이 이해되지 않아요": [
        "1. 이해하기 어려운 부분을 확인합니다.",
        "2. '더 쉬운 말로 설명해 줘'라고 요청합니다.",
        "3. 한 번에 한 가지씩 질문합니다.",
        "4. 이해가 될 때까지 다시 질문합니다."
    ],
    "AI 답변이 맞는지 확인하기": [
        "1. AI가 알려 준 내용 중 중요한 정보를 확인합니다.",
        "2. 공공기관이나 공식 홈페이지에서 찾아봅니다.",
        "3. 다른 자료와 비교합니다.",
        "4. 건강이나 돈과 관련된 중요한 문제는 전문가에게 확인합니다."
    ]
}

st.subheader("📘 사용 방법")

for step in guides[menu]:
    st.write(step)

st.divider()

st.subheader("🔎 내 상황에 맞는 안내 찾기")

question = st.text_input(
    "어려운 점을 입력하세요.",
    placeholder="예: 사진을 어떻게 올리는지 모르겠어요."
)

if st.button("안내 찾기"):
    if not question.strip():
        st.warning("어려운 점을 먼저 입력해 주세요.")
    else:
        q = question.lower()

        if any(word in q for word in ["사진", "이미지", "파일", "첨부"]):
            result = "사진 올리기"
        elif any(word in q for word in ["음성", "마이크", "말하기", "목소리"]):
            result = "음성으로 질문하기"
        elif any(word in q for word in ["틀린", "정확", "사실", "거짓", "확인"]):
            result = "AI 답변이 맞는지 확인하기"
        elif any(word in q for word in ["이해", "어려워", "모르겠"]):
            result = "답변이 이해되지 않아요"
        else:
            result = "AI에게 질문하기"

        st.success(f"추천 안내: {result}")

        for step in guides[result]:
            st.write(step)

st.divider()

st.subheader("🔐 안전하게 AI 사용하기")

st.warning(
    "비밀번호와 주민등록번호 같은 개인정보는 입력하지 마세요. "
    "AI의 답변은 틀릴 수 있으므로 중요한 정보는 꼭 확인하세요."
)

st.caption("AI 사용 안내 시스템 | 초보자를 위한 쉬운 AI 사용 가이드")
