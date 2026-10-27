
import streamlit as st

# -------------------------------
# 1. 기본 화면 설정
# -------------------------------
st.set_page_config(
    page_title="AI 사용 안내 시스템",
    page_icon="💡",
    layout="centered"
)

# 큰 글씨와 간단한 화면 구성
st.markdown("""
<style>
html, body, [class*="st-"] {
    font-size: 20px !important;
}
h1 {
    font-size: 34px !important;
}
h2 {
    font-size: 28px !important;
}
h3 {
    font-size: 23px !important;
}
.stButton button {
    min-height: 55px;
    font-size: 19px !important;
    border-radius: 12px;
}
div[data-testid="stTextInput"] input {
    min-height: 50px;
    font-size: 19px;
}
</style>
""", unsafe_allow_html=True)

st.title("💡 AI 사용 안내 시스템")
st.write("AI 사용이 어렵다면 아래에서 필요한 도움을 찾아보세요.")
st.info("처음 사용하는 분도 쉽게 따라 할 수 있도록 안내해 드립니다.")

# -------------------------------
# 2. 상황별 안내 자료
# -------------------------------
guides = {
    "AI에게 질문하기": {
        "keywords": [
            "질문", "입력", "물어", "글쓰기",
            "사용법", "시작", "처음", "ai 사용"
        ],
        "steps": [
            "AI 서비스에 접속합니다.",
            "화면 아래쪽의 질문 입력창을 찾습니다.",
            "궁금한 내용을 짧고 구체적으로 입력합니다.",
            "보내기 버튼을 누릅니다.",
            "답변을 읽고 이해되지 않는 부분은 다시 질문합니다."
        ],
        "example": "예시: 스마트폰으로 사진을 보내는 방법을 쉽게 알려 줘."
    },
    "사진 및 파일 올리기": {
        "keywords": [
            "사진", "이미지", "파일", "첨부", "그림", "사진 올리"
        ],
        "steps": [
            "질문 입력창 근처의 + 또는 첨부 버튼을 찾습니다.",
            "사진이나 파일 선택을 누릅니다.",
            "기기에 저장된 파일을 선택합니다.",
            "사진과 함께 궁금한 내용을 입력합니다.",
            "보내기 버튼을 누르고 답변을 확인합니다."
        ],
        "example": "예시: 이 사진에 무엇이 있는지 쉽게 설명해 줘."
    },
    "음성으로 질문하기": {
        "keywords": [
            "음성", "마이크", "말하기", "말로",
            "목소리", "말을", "듣기"
        ],
        "steps": [
            "마이크 또는 음성 대화 버튼을 찾습니다.",
            "기기에서 마이크 사용을 허용합니다.",
            "버튼을 누르고 궁금한 내용을 말합니다.",
            "AI의 답변을 듣거나 화면에서 읽습니다."
        ],
        "example": "예시: 오늘 해야 할 일을 정리하는 방법을 알려 줘."
    },
    "답변 쉽게 이해하기": {
        "keywords": [
            "이해", "어려워", "무슨 뜻", "모르겠",
            "쉽게", "설명", "짧게"
        ],
        "steps": [
            "이해하기 어려운 부분을 확인합니다.",
            "AI에게 쉬운 말로 다시 설명해 달라고 요청합니다.",
            "한 번에 한 가지씩 질문합니다.",
            "필요하면 예시를 들어 달라고 요청합니다."
        ],
        "example": "예시: 어려운 단어를 빼고 쉽게 설명해 줘."
    },
    "오류 해결하기": {
        "keywords": [
            "오류", "안돼", "안 돼", "멈춤",
            "고장", "접속", "실행", "작동", "느려"
        ],
        "steps": [
            "인터넷 연결 상태를 확인합니다.",
            "화면을 새로고침합니다.",
            "앱이나 인터넷 브라우저를 다시 실행합니다.",
            "로그인 상태를 확인합니다.",
            "문제가 계속되면 화면에 표시된 오류 내용을 확인합니다."
        ],
        "example": "비밀번호를 다른 사람에게 알려 주지 말고 공식 고객센터에 문의하세요."
    },
    "개인정보 보호하기": {
        "keywords": [
            "개인정보", "비밀번호", "주민등록",
            "계좌", "보안", "안전", "주소", "사기"
        ],
        "steps": [
            "주민등록번호나 비밀번호를 입력하지 않습니다.",
            "계좌번호와 집 주소 등 중요한 정보도 공유하지 않습니다.",
            "모르는 사람이 보낸 링크는 조심합니다.",
            "개인정보를 요구하는 화면은 신중하게 확인합니다."
        ],
        "example": "개인정보가 노출되었다고 의심되면 해당 서비스의 공식 고객센터에 문의하세요."
    },
    "AI 답변 확인하기": {
        "keywords": [
            "틀린", "정확", "사실", "거짓",
            "출처", "믿어", "확인", "진짜"
        ],
        "steps": [
            "AI가 알려 준 내용에 근거가 있는지 확인합니다.",
            "공공기관이나 공식 홈페이지에서 다시 찾아봅니다.",
            "날짜와 숫자 등 중요한 정보를 비교합니다.",
            "건강이나 법률처럼 중요한 문제는 전문가에게 문의합니다."
        ],
        "example": "AI가 알려 준 내용이 항상 정확한 것은 아닙니다."
    }
}

# -------------------------------
# 3. 안내 표시 함수
# -------------------------------
def show_guide(topic):
    guide = guides.get(topic)

    if guide is None:
        st.error("안내 자료를 찾을 수 없습니다.")
        return

    st.subheader("📘 " + topic)
    st.write("아래 순서대로 따라 해 보세요.")

    for i, step in enumerate(guide["steps"], start=1):
        st.markdown(f"**{i}단계.** {step}")

    st.success(guide["example"])


# -------------------------------
# 4. 상황별 빠른 안내 버튼
# -------------------------------
st.header("1. 필요한 도움 선택하기")

topics = list(guides.keys())

for start in range(0, len(topics), 2):
    columns = st.columns(2)

    for offset, column in enumerate(columns):
        index = start + offset

        if index < len(topics):
            topic = topics[index]

            with column:
                if st.button(
                    topic,
                    key=f"button_{index}",
                    use_container_width=True
                ):
                    st.session_state["selected_topic"] = topic

if "selected_topic" in st.session_state:
    show_guide(st.session_state["selected_topic"])

st.divider()

# -------------------------------
# 5. 직접 질문하고 맞춤 안내 받기
# -------------------------------
st.header("2. 직접 질문하기")
st.write("어떤 점이 어려운지 입력하면 관련된 안내를 찾아 드립니다.")

with st.form("question_form"):
    question = st.text_input(
        "궁금한 내용",
        placeholder="예: 사진을 어떻게 올리는지 모르겠어요."
    )

    submitted = st.form_submit_button(
        "안내 찾아보기",
        use_container_width=True
    )

if submitted:
    q = question.strip().lower()

    if not q:
        st.warning("질문을 먼저 입력해 주세요.")

    else:
        # 질문과 안내 자료의 관련 단어를 비교합니다.
        scores = {}

        for topic, guide in guides.items():
            score = sum(
                1 for keyword in guide["keywords"]
                if keyword in q
            )
            scores[topic] = score

        best_topic = max(scores, key=scores.get)

        if scores[best_topic] > 0:
            st.session_state["answer_topic"] = best_topic
            st.session_state["answer_question"] = question.strip()
        else:
            st.session_state["answer_topic"] = None
            st.session_state["answer_question"] = question.strip()

if "answer_question" in st.session_state:
    st.markdown("### 💬 질문 결과")
    st.write("입력한 질문: " + st.session_state["answer_question"])

    answer_topic = st.session_state["answer_topic"]

    if answer_topic:
        show_guide(answer_topic)
    else:
        st.warning(
            "질문과 정확히 맞는 안내를 찾지 못했습니다. "
            "위의 상황별 안내 버튼에서 비슷한 항목을 선택하거나 "
            "다른 표현으로 질문해 주세요."
        )

st.divider()

# -------------------------------
# 6. 개인정보 보호 안내
# -------------------------------
st.header("3. 안전하게 AI 사용하기")

with st.expander("🔐 개인정보 보호 방법"):
    st.write(
        "주민등록번호, 비밀번호, 계좌번호, 집 주소 등 "
        "중요한 개인정보를 AI에 입력하지 마세요."
    )

with st.expander("✅ AI 답변 확인 방법"):
    st.write(
        "AI는 잘못된 정보를 알려 줄 수 있습니다. "
        "중요한 정보는 공공기관이나 공식 홈페이지에서 확인하세요."
    )

with st.expander("🛠️ 문제가 생겼을 때"):
    st.write(
        "인터넷 연결을 확인하고 앱을 다시 실행해 보세요. "
        "문제가 지속되면 해당 서비스의 공식 고객센터에 문의하세요."
    )

st.caption("AI 사용 안내 시스템 | 누구나 쉽게 배우는 AI 사용법")
