
import streamlit as st

st.set_page_config(
    page_title="AI 사용 안내 시스템",
    page_icon="💡",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px;
}
.stButton button {
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

st.title("💡 AI 사용 안내 시스템")
st.write("AI 사용이 어렵다면 편하게 질문해 보세요!")
st.info("AI 초보자와 어르신을 위한 쉬운 사용 안내 서비스입니다.")

# 안내 자료
GUIDES = {
    "질문하기": {
        "keywords": ["질문", "입력", "글쓰기", "물어", "검색"],
        "answer": (
            "📝 AI에게 질문하는 방법\n\n"
            "1. AI 서비스에 접속하세요.\n"
            "2. 화면 아래쪽의 입력창을 찾으세요.\n"
            "3. 궁금한 내용을 입력하세요.\n"
            "4. 보내기 버튼을 누르세요.\n\n"
            "예시: 스마트폰 사용법을 쉽게 알려 줘."
        )
    },
    "사진 올리기": {
        "keywords": ["사진", "이미지", "파일", "첨부"],
        "answer": (
            "📷 사진 올리는 방법\n\n"
            "1. 입력창 옆의 + 또는 첨부 버튼을 찾으세요.\n"
            "2. 사진이나 파일 선택을 누르세요.\n"
            "3. 원하는 사진을 선택하세요.\n"
            "4. 사진과 함께 궁금한 내용을 입력하세요.\n"
            "5. 보내기 버튼을 누르세요.\n\n"
            "서비스마다 버튼의 위치와 지원 기능이 다를 수 있어요."
        )
    },
    "음성 사용": {
        "keywords": ["음성", "마이크", "말하기", "말로", "목소리"],
        "answer": (
            "🎤 음성으로 질문하는 방법\n\n"
            "1. 마이크 또는 음성 대화 버튼을 찾으세요.\n"
            "2. 마이크 사용을 허용하세요.\n"
            "3. 버튼을 누르고 질문을 말하세요.\n"
            "4. 답변을 듣거나 화면에서 확인하세요.\n\n"
            "음성 기능은 서비스와 기기에 따라 지원 여부가 달라요."
        )
    },
    "답변 이해하기": {
        "keywords": ["이해", "어려워", "무슨 뜻", "모르겠", "설명"],
        "answer": (
            "📖 답변을 쉽게 이해하는 방법\n\n"
            "AI에게 다음과 같이 다시 요청해 보세요.\n\n"
            "• 어려운 단어 없이 설명해 줘.\n"
            "• 중요한 내용만 짧게 알려 줘.\n"
            "• 순서대로 하나씩 설명해 줘.\n"
            "• 예시를 들어 설명해 줘."
        )
    },
    "오류 해결": {
        "keywords": ["오류", "안돼", "안 돼", "작동", "멈춤", "고장", "접속"],
        "answer": (
            "🛠️ 문제가 생겼을 때 해결 방법\n\n"
            "1. 인터넷 연결을 확인하세요.\n"
            "2. 화면을 새로고침하세요.\n"
            "3. 앱이나 브라우저를 다시 실행하세요.\n"
            "4. 로그인 상태를 확인하세요.\n"
            "5. 계속 문제가 생기면 오류 메시지를 확인하세요.\n\n"
            "비밀번호를 다른 사람에게 알려 주지는 마세요."
        )
    },
    "개인정보 보호": {
        "keywords": ["개인정보", "비밀번호", "주민등록", "계좌", "안전", "보안"],
        "answer": (
            "🔐 개인정보 보호 방법\n\n"
            "1. 비밀번호와 주민등록번호를 입력하지 마세요.\n"
            "2. 계좌번호나 집 주소도 함부로 공유하지 마세요.\n"
            "3. 모르는 사람이 보낸 링크는 조심하세요.\n"
            "4. AI가 알려 주는 중요한 정보는 공식 자료로 확인하세요."
        )
    },
    "답변 확인": {
        "keywords": ["틀린", "정확", "사실", "믿어", "거짓", "출처"],
        "answer": (
            "🔎 AI 답변 확인 방법\n\n"
            "1. 답변에 근거 자료가 있는지 확인하세요.\n"
            "2. 정부 기관이나 공식 홈페이지에서 다시 찾아보세요.\n"
            "3. 날짜와 숫자가 정확한지 확인하세요.\n"
            "4. 건강이나 법률 등 중요한 문제는 전문가에게 문의하세요.\n\n"
            "AI도 틀린 정보를 알려 줄 수 있어요."
        )
    }
}


def get_answer(question):
    """질문에 맞는 안내 자료를 찾아 반환합니다."""
    q = question.strip().lower()

    if not q:
        return "질문을 입력해 주세요."

    # 질문에 포함된 단어를 바탕으로 안내 주제를 찾습니다.
    for topic, data in GUIDES.items():
        if any(word in q for word in data["keywords"]):
            return data["answer"]

    return (
        "🤝 질문을 정확히 이해하지 못했어요.\n\n"
        "아래 주제 중 하나를 선택해 보세요.\n\n"
        "• AI에게 질문하는 방법\n"
        "• 사진이나 파일 올리는 방법\n"
        "• 음성으로 질문하는 방법\n"
        "• 오류 해결 방법\n"
        "• 개인정보 보호 방법\n\n"
        "어떤 상황인지 조금 더 구체적으로 입력해 주셔도 좋아요."
    )


# 빠른 안내 버튼
st.subheader("📌 필요한 도움을 선택하세요.")

buttons = st.columns(2)

topics = list(GUIDES.keys())

for i, topic in enumerate(topics):
    with buttons[i % 2]:
        if st.button(topic, key=f"topic_{i}", use_container_width=True):
            st.session_state["last_question"] = topic
            st.session_state["last_answer"] = GUIDES[topic]["answer"]

# 버튼을 눌렀을 때 선택한 안내 표시
if "last_answer" in st.session_state:
    st.markdown("### 📘 안내 결과")
    st.markdown(st.session_state["last_answer"])

st.divider()

# 질문 입력 기능
st.subheader("💬 직접 질문하기")
st.write("궁금하거나 어려운 점을 아래에 입력하세요.")

with st.form("question_form", clear_on_submit=True):
    question = st.text_input(
        "질문 내용",
        placeholder="예: 사진을 어떻게 올려요?"
    )
    submitted = st.form_submit_button(
        "답변 확인하기",
        use_container_width=True
    )

if submitted:
    if not question.strip():
        st.warning("질문을 먼저 입력해 주세요.")
    else:
        st.session_state["last_question"] = question
        st.session_state["last_answer"] = get_answer(question)

if (
    "last_question" in st.session_state
    and "last_answer" in st.session_state
):
    st.markdown("### 💡 질문에 대한 안내")
    st.chat_message("user").write(
        st.session_state["last_question"]
    )
    st.chat_message("assistant").write(
        st.session_state["last_answer"]
    )

st.divider()

with st.expander("🔒 AI를 안전하게 사용하는 방법"):
    st.write(
        "개인정보를 입력하지 마세요. "
        "AI가 알려 주는 정보는 틀릴 수 있으므로 "
        "중요한 내용은 공식 자료로 확인하세요."
    )

st.caption("AI 사용 안내 시스템 | 초보자를 위한 쉬운 안내")
