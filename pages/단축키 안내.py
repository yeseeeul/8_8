
import os
import uuid
import json

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types


st.set_page_config(
    page_title="AI 단축키 제작소",
    page_icon="⌨️",
    layout="wide",
)

MODEL_NAME = "gemini-2.5-flash-lite"

PRESETS = {
    "요약하기": "다음 글의 핵심 내용을 한국어로 간결하게 요약해 줘.",
    "맞춤법 교정": "다음 글의 맞춤법과 띄어쓰기를 교정해 줘. 수정된 글만 보여 줘.",
    "영어로 번역": "다음 글을 자연스러운 영어로 번역해 줘.",
    "한국어로 번역": "다음 글을 자연스러운 한국어로 번역해 줘.",
    "글 다듬기": "다음 글의 의미를 유지하면서 자연스럽고 읽기 쉽게 다듬어 줘.",
    "핵심 키워드": "다음 글의 핵심 키워드 5개와 설명을 알려 줘.",
    "직접 작성": "",
}


def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.environ.get("GEMINI_API_KEY", "")


def normalize_shortcut(value):
    parts = [p.strip().lower() for p in value.split("+") if p.strip()]
    aliases = {
        "control": "ctrl",
        "ctrl": "ctrl",
        "shift": "shift",
        "alt": "alt",
        "option": "alt",
        "cmd": "meta",
        "command": "meta",
        "meta": "meta",
    }
    parts = [aliases.get(p, p) for p in parts]

    modifiers = []
    key = None

    for part in parts:
        if part in ("ctrl", "shift", "alt", "meta"):
            if part not in modifiers:
                modifiers.append(part)
        else:
            if key is not None:
                raise ValueError("일반 키는 하나만 지정해 주세요.")
            key = part

    if not key:
        raise ValueError("Ctrl+Shift+S처럼 일반 키를 포함해 주세요.")

    order = ["ctrl", "alt", "shift", "meta"]
    result = [m for m in order if m in modifiers] + [key]
    return "+".join(result)


def call_gemini(instruction, user_text):
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "API 키가 없습니다. Streamlit Cloud의 Settings → Secrets에서 "
            "GEMINI_API_KEY를 설정해 주세요."
        )

    if not user_text.strip():
        raise ValueError("AI에게 전달할 텍스트를 먼저 입력해 주세요.")

    prompt = (
        "너는 사용자의 작업을 돕는 AI 비서야.\n\n"
        f"[작업 지시]\n{instruction}\n\n"
        f"[사용자 입력]\n{user_text}"
    )

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30000),
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    result = getattr(response, "text", None)

    if not result or not result.strip():
        raise RuntimeError("AI가 결과를 반환하지 않았습니다. 다시 시도해 주세요.")

    return result.strip()


# 세션 데이터 초기화
if "shortcuts" not in st.session_state:
    st.session_state.shortcuts = [
        {
            "id": "summary",
            "name": "빠른 요약",
            "key": "ctrl+shift+s",
            "action": "요약하기",
            "instruction": PRESETS["요약하기"],
        },
        {
            "id": "proofread",
            "name": "맞춤법 검사",
            "key": "ctrl+shift+g",
            "action": "맞춤법 교정",
            "instruction": PRESETS["맞춤법 교정"],
        },
        {
            "id": "translate",
            "name": "영어 번역",
            "key": "ctrl+shift+e",
            "action": "영어로 번역",
            "instruction": PRESETS["영어로 번역"],
        },
    ]

if "ai_result" not in st.session_state:
    st.session_state.ai_result = ""

if "last_task" not in st.session_state:
    st.session_state.last_task = ""

if "history" not in st.session_state:
    st.session_state.history = []


# 다크모드 및 라이트모드 대응 디자인
st.markdown(
    """
    <style>
    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .hero {
        padding: 28px;
        border-radius: 20px;
        color: #ffffff !important;
        background: linear-gradient(120deg, #28245e, #6655cc);
        margin-bottom: 22px;
    }

    .hero h1, .hero p {
        color: #ffffff !important;
    }

    .hero h1 {
        font-size: 2rem;
        margin-bottom: 8px;
    }

    .hero p {
        margin-bottom: 0;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--border-color);
        border-radius: 14px;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--text-color);
        opacity: 0.85;
    }

    [data-testid="stCode"],
    [data-testid="stCode"] pre {
        background-color: var(--secondary-background-color) !important;
        color: var(--text-color) !important;
    }

    input, textarea {
        color: var(--text-color) !important;
    }

    [data-baseweb="select"] > div {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
    }

    .stButton > button,
    .stDownloadButton > button,
    [data-testid="stFormSubmitButton"] button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 2.5rem;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 상단 배너
st.markdown(
    """
    <div class="hero">
        <h1>⌨️ AI 단축키 제작소</h1>
        <p>반복하는 작업을 단축키 하나로 해결하세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

api_ready = bool(get_api_key())

col1, col2 = st.columns(2)
col1.metric("등록된 단축키", len(st.session_state.shortcuts))
col2.metric(
    "Gemini API",
    "설정 완료" if api_ready else "키 설정 필요",
)

if not api_ready:
    st.info(
        "AI 기능을 사용하려면 Streamlit Cloud의 "
        "Settings → Secrets에 GEMINI_API_KEY를 등록하세요."
    )


# 입력 영역
st.subheader("✍️ AI 작업 입력")

user_text = st.text_area(
    "AI에게 전달할 텍스트",
    placeholder="요약할 글, 번역할 문장, 다듬을 내용을 입력하세요.",
    height=170,
    key="user_text",
)

st.caption("원하는 작업의 실행 버튼을 누르거나 키보드 단축키를 사용하세요.")


# 등록된 단축키
st.subheader("⚡ 등록된 단축키")

for item in list(st.session_state.shortcuts):
    with st.container(border=True):
        col_info, col_run, col_delete = st.columns([3, 2, 1])

        with col_info:
            st.markdown(f"**{item['name']}**")
            st.code(item["key"], language=None)
            st.caption(item["action"])

        with col_run:
            run_clicked = st.button(
                f"⚡ 실행: {item['name']}",
                key=f"run_{item['id']}",
                use_container_width=True,
            )

        with col_delete:
            delete_clicked = st.button(
                "삭제",
                key=f"delete_{item['id']}",
                use_container_width=True,
            )

        if delete_clicked:
            st.session_state.shortcuts = [
                s for s in st.session_state.shortcuts
                if s["id"] != item["id"]
            ]
            st.rerun()

        if run_clicked:
            try:
                with st.spinner("AI가 작업 중입니다..."):
                    result = call_gemini(
                        item["instruction"],
                        user_text,
                    )

                st.session_state.ai_result = result
                st.session_state.last_task = item["name"]
                st.session_state.history.insert(
                    0,
                    {"name": item["name"], "result": result},
                )
                st.session_state.history = st.session_state.history[:10]

                st.success("AI 작업이 완료되었습니다.")

            except ValueError as exc:
                st.warning(str(exc))

            except RuntimeError as exc:
                st.error(str(exc))

            except Exception as exc:
                message = str(exc).lower()

                if any(x in message for x in (
                    "api_key", "api key", "unauthorized",
                    "permission denied", "invalid api key",
                )):
                    st.error("API 키가 잘못되었거나 권한이 없습니다.")

                elif any(x in message for x in (
                    "429", "resource_exhausted", "quota",
                )):
                    st.error("API 사용 한도에 도달했습니다. 잠시 후 다시 시도하세요.")

                elif "timeout" in message or "timed out" in message:
                    st.error("AI 응답 시간이 초과되었습니다. 다시 시도하세요.")

                else:
                    st.error("AI 실행 중 오류가 발생했습니다.")
                    with st.expander("오류 상세 정보"):
                        st.code(str(exc)[:1500])


# AI 결과
st.divider()
st.subheader("🪄 AI 실행 결과")

if st.session_state.ai_result:
    st.caption(f"마지막 작업: {st.session_state.last_task}")

    st.text_area(
        "결과",
        value=st.session_state.ai_result,
        height=250,
        key="result_display",
    )

    st.download_button(
        "📥 결과를 TXT 파일로 저장",
        data=st.session_state.ai_result,
        file_name="ai_result.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.caption("아직 결과가 없습니다.")


# 새 단축키 만들기
st.divider()
st.subheader("➕ 나만의 AI 단축키 만들기")

with st.form("create_shortcut_form", clear_on_submit=True):
    new_name = st.text_input(
        "단축키 이름",
        placeholder="예: 수행평가 문장 다듬기",
    )

    new_key_input = st.text_input(
        "원하는 키 조합",
        placeholder="예: Ctrl+Shift+W",
    )

    new_action = st.selectbox(
        "AI 기능",
        list(PRESETS.keys()),
    )

    custom_instruction = st.text_area(
        "AI에게 시킬 작업",
        placeholder="예: 중학생이 이해하기 쉽게 설명해 줘.",
        height=100,
    )

    submitted = st.form_submit_button(
        "단축키 등록하기",
        type="primary",
        use_container_width=True,
    )

if submitted:
    try:
        name = new_name.strip()

        if not name:
            raise ValueError("단축키 이름을 입력해 주세요.")

        if not new_key_input.strip():
            raise ValueError("키 조합을 입력해 주세요.")

        normalized_key = normalize_shortcut(new_key_input)

        if any(
            s["key"] == normalized_key
            for s in st.session_state.shortcuts
        ):
            raise ValueError("이미 등록된 단축키입니다.")

        instruction = custom_instruction.strip() or PRESETS[new_action]

        if not instruction:
            raise ValueError("AI에게 시킬 작업 내용을 입력해 주세요.")

        st.session_state.shortcuts.append({
            "id": uuid.uuid4().hex[:12],
            "name": name,
            "key": normalized_key,
            "action": new_action,
            "instruction": instruction,
        })

        st.success(f"'{name}' 단축키가 등록되었습니다.")
        st.rerun()

    except ValueError as exc:
        st.error(str(exc))


# 키보드 단축키 감지
shortcut_map = [
    {"key": s["key"], "name": s["name"]}
    for s in st.session_state.shortcuts
]

shortcut_map_json = json.dumps(shortcut_map, ensure_ascii=False)

components.html(
    f"""
    <script>
    (() => {{
        try {{
            const doc = window.parent.document;

            if (window.parent.__aiShortcutHandler) {{
                doc.removeEventListener(
                    "keydown",
                    window.parent.__aiShortcutHandler,
                    true
                );
            }}

            const shortcuts = {shortcut_map_json};

            const handler = (event) => {{
                const target = event.target;
                const tag = target && target.tagName
                    ? target.tagName.toLowerCase() : "";

                const typing =
                    tag === "textarea" ||
                    tag === "input" ||
                    (target && target.isContentEditable);

                if (typing) return;

                for (const shortcut of shortcuts) {{
                    const parts = shortcut.key.split("+");
                    const key = parts[parts.length - 1];

                    const matched =
                        event.ctrlKey === parts.includes("ctrl") &&
                        event.altKey === parts.includes("alt") &&
                        event.shiftKey === parts.includes("shift") &&
                        event.metaKey === parts.includes("meta") &&
                        event.key.toLowerCase() === key;

                    if (!matched) continue;

                    const buttons = Array.from(
                        doc.querySelectorAll("button")
                    );

                    const button = buttons.find(
                        b => b.innerText.includes(
                            "실행: " + shortcut.name
                        )
                    );

                    if (button) {{
                        event.preventDefault();
                        button.click();
                    }}

                    break;
                }}
            }};

            window.parent.__aiShortcutHandler = handler;
            doc.addEventListener("keydown", handler, true);

        }} catch (error) {{
            // 브라우저 제한 시 화면의 실행 버튼을 사용합니다.
        }}
    }})();
    </script>
    """,
    height=0,
)


# 최근 실행 기록
with st.expander("🕘 최근 실행 기록"):
    if st.session_state.history:
        for index, entry in enumerate(
            st.session_state.history,
            start=1,
        ):
            st.markdown(f"**{index}. {entry['name']}**")
            st.text(entry["result"][:500])

            if len(entry["result"]) > 500:
                st.caption("미리보기입니다. 전체 결과는 위에서 확인하세요.")

            st.divider()
    else:
        st.caption("아직 실행 기록이 없습니다.")


st.caption(
    "개인정보 보호: 입력한 텍스트는 AI 처리를 위해 Google Gemini API로 전송됩니다. "
    "비밀번호나 인증 정보 등 민감한 내용은 입력하지 마세요."
)
