
import html
import streamlit as st

st.set_page_config(
    page_title="큰글씨 | 글씨 크기 확대",
    page_icon="🔎",
    layout="wide",
)

# 화면 디자인
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.6rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #e8f2ff, #f4efff);
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        margin: 0;
        color: #172b4d;
        font-size: 2.2rem;
    }
    .hero p {
        margin: 0.6rem 0 0 0;
        color: #344563;
        font-size: 1rem;
    }
    .preview {
        padding: 28px;
        border: 1px solid #d9dee8;
        border-radius: 16px;
        min-height: 240px;
        overflow-wrap: anywhere;
        word-break: break-word;
    }
    .small-note {
        color: #64748b;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🔎 큰글씨</h1>
        <p>작은 글씨가 불편하다면, 원하는 크기로 키워 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("### 1. 확대할 글 입력하기")

text_input = st.text_area(
    "내용",
    placeholder="여기에 확대하고 싶은 글을 입력하세요.",
    height=150,
    label_visibility="collapsed",
    key="user_text",
)

st.write("### 2. 글씨 설정")

left, right = st.columns(2)

with left:
    font_size = st.slider(
        "글씨 크기",
        min_value=16,
        max_value=64,
        value=32,
        step=2,
        format="%d px",
    )

    line_height = st.slider(
        "줄 간격",
        min_value=1.2,
        max_value=2.4,
        value=1.7,
        step=0.1,
        format="%.1f",
    )

with right:
    text_color = st.selectbox(
        "글자색",
        options=["검정", "진한 파랑", "진한 초록", "흰색"],
        index=0,
    )

    background_color = st.selectbox(
        "배경색",
        options=["흰색", "연한 노랑", "연한 파랑", "검정"],
        index=0,
    )

color_map = {
    "검정": "#111111",
    "진한 파랑": "#123A70",
    "진한 초록": "#14532D",
    "흰색": "#FFFFFF",
}

background_map = {
    "흰색": "#FFFFFF",
    "연한 노랑": "#FFF7D6",
    "연한 파랑": "#EAF4FF",
    "검정": "#111111",
}

# 검정 배경에서는 흰색 글자를 기본으로 선택
if background_color == "검정" and text_color != "흰색":
    st.info("검정 배경에서는 글자가 잘 보이도록 흰색 글자를 선택해 보세요.")

st.divider()
st.write("### 3. 확대된 글씨 미리보기")

if text_input.strip():
    safe_text = html.escape(text_input)
    font_color = color_map[text_color]
    background = background_map[background_color]

    st.markdown(
        f"""
        <div class="preview" style="
            font-size: {font_size}px;
            line-height: {line_height};
            color: {font_color};
            background-color: {background};
            white-space: pre-wrap;
            font-family: sans-serif;
        ">{safe_text}</div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"글자 크기: {font_size}px · 줄 간격: {line_height:.1f}"
    )

    st.write("### 4. 복사하거나 저장하기")

    st.caption("아래 텍스트 상자의 복사 버튼을 누르면 원문을 복사할 수 있습니다.")
    st.code(text_input, language=None)

    st.download_button(
        label="📥 글 저장하기 (.txt)",
        data=text_input.encode("utf-8-sig"),
        file_name="큰글씨_텍스트.txt",
        mime="text/plain; charset=utf-8",
        use_container_width=True,
    )
else:
    st.info("위 입력창에 글을 입력하면 확대된 글씨가 여기에 표시됩니다.")

    st.markdown(
        """
        <div class="preview" style="
            font-size: 28px;
            line-height: 1.7;
            color: #64748b;
            background: #f8fafc;
        ">
            여기에 큰 글씨가 표시됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.markdown(
    '<p class="small-note">큰글씨 · 누구나 편하게 읽을 수 있는 글씨 확대 도구</p>',
    unsafe_allow_html=True,
)

