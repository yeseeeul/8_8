
import os
import json
import uuid
import re

import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="AI 단축키 제작소",
    page_icon="⌨️",
    layout="wide",
)

MODEL_NAME = "gemini-2.5-flash-lite"

PRESETS = {
    "요약하기": "다음 글의 핵심 내용을 한국어로 간결하게 요약해 줘.",
    "맞춤법 교정": "다음 글의 맞춤법, 띄어쓰기, 문법을 교정해 줘. 수정된 글만 보여 줘.",
    "영어로 번역": "다음 글을 자연스러운 영어로 번역해 줘.",
    "한국어로 번역": "다음 글을 자연스러운 한국어로 번역해 줘.",
    "글 다듬기": "다음 글을 의미는 유지하면서 더 자연스럽고 읽기 쉽게 다듬어 줘.",
    "핵심 키워드": "다음 글의 핵심 키워드 5개와 각각의 간단한 설명을 알려 줘.",
    "직접 작성": "",
}


def normalize_shortcut(value):
    """Ctrl+Shift+S 형식의 단축키를 정규화한다."""
    parts = [p.strip().lower() for p in value.split("+") if p.strip()]
    aliases = {
        "ctrl": "ctrl",
        "control": "ctrl",
        "shift": "shift",
        "alt": "alt",
        "option": "alt",
        "cmd": "meta",
        "command": "meta",
        "meta": "meta",
    }

    modifiers = []
    key = None

    for part in parts:
        part = aliases.get(part, part)
        if part in ("ctrl", "shift", "alt", "meta"):
            if part not in modifiers:
                modifiers.append(part)
        else:
            if key is not None:
                raise ValueError("단축키에는 일반 키를 하나만 지정할 수 있습니다.")
            key = part

    if key is None:
        raise ValueError("Ctrl+Shift+S처럼 일반 키를 하나 포함해 주세요.")

    if key in ("ctrl", "shift", "alt", "meta"):
        raise ValueError("Ctrl, Shift, Alt만으로는 단축키를 만들 수 없습니다.")

    order = ["ctrl", "alt", "shift", "meta"]
    return "+".join([m for m in order if m in modifiers] + [key])


def get_api_key():
    """Streamlit Secrets 또는 환경 변수에서 API 키를 읽는다."""
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""

    return secret_key or os.environ.get("GEMINI_API_KEY", "")


def call_gemini(instruction, user_text):
    """Gemini API를 호출하고 오류를 사용자에게 이해하기 쉽게 전달한다."""
    api_key = get_api_key()

    if not api_key:
        raise RuntimeError(
            "Gemini API 키가 없습니다. "
            "Streamlit Cloud의 Settings → Secrets에서 "
            "GEMINI_API_KEY를 설정해 주세요."
        )

    if not user_text.strip():
        raise ValueError("AI에게 보낼 내용을 먼저 입력해 주세요.")

    prompt = (
        "너는 사용자의 작업을 돕는 AI 비서야.\n"
        "아래 지시를 정확하게 수행해 줘.\n\n"
        f"[작업 지시]\n{instruction.strip()}\n\n"
        f"[사용자 입력]\n{user_text.strip()}"
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
        raise RuntimeError(
            "AI가 결과를 반환하지 않았습니다. 입력 내용을 바꾸어 다시 시도해 주세요."
        )

    return result.strip()


# -----------------------------
# 세션 초기화
# -----------------------------
if "shortcuts" not in st.session_state:
    st.session_state.shortcuts = [
        {
            "id": "preset_summary",
            "name": "빠른 요약",
            "key": "ctrl+shift+s",
            "action": "요약하기",
            "instruction": PRESETS["요약하기"],
        },
        {
            "id": "preset_proofread",
            "name": "맞춤법 검사",
            "key": "ctrl+shift+g",
            "action": "맞춤법 교정",
            "instruction": PRESETS["맞춤법 교정"],
        },
        {
            "id": "preset_translate",
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


# -----------------------------
# 디자인
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7f7ff 0%, #ffffff 42%);
    }
    .hero {
        padding: 28px;
        border-radius: 22px;
        color: white;
        background: linear-gradient(120deg, #28245e, #6655cc);
        margin-bottom: 22px;
    }
    .hero h1 {
        color: white;
        margin-bottom: 8px;
        font-size: 2.1rem;
    }
    .hero p {
        color: #e6e2ff;
        margin-bottom: 0;
    }
    .hint {
        color: #686b80;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>⌨️ AI 단축키 제작소</h1>
      <p>반복하는 작업을 단축키 하나로. 나만의 AI 도구를 만들어 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 앱 상태 안내
api_ready = bool(get_api_key())
status_col1, status_col2 = st.columns(2)

with status_col1:
    st.metric("등록된 단축키", len(st.session_state.shortcuts))

with status_col2:
    st.metric("Gemini API", "연결 설정됨" if api_ready else "키 설정 필요")

if not api_ready:
    st.info(
        "앱은 사용할 수 있지만 AI 실행에는 Gemini API 키가 필요합니다. "
        "아래 배포 안내의 Secrets 설정을 완료해 주세요."
    )


# -----------------------------
# 입력 영역
# -----------------------------
st.subheader("✍️ AI 작업 입력")

user_text = st.text_area(
    "AI에게 전달할 텍스트",
    placeholder="요약할 글, 번역할 문장, 다듬을 내용을 입력하세요.",
    height=180,
    key="user_text",
)

st.caption("아래에서 단축키를 선택해 실행하거나, 직접 만든 작업을 등록할 수 있습니다.")


# -----------------------------
# 단축키 실행
# -----------------------------
st.subheader("⚡ 등록된 단축키")

shortcuts = st.session_state.shortcuts

if not shortcuts:
    st.info("등록된 단축키가 없습니다. 아래에서 새 단축키를 만들어 보세요.")

for item in shortcuts:
    with st.container(border=True):
        col_info, col_action, col_delete = st.columns([3, 2, 1])

        with col_info:
            st.markdown(f"**{item['name']}**")
            st.code(item["key"], language=None)
            st.caption(item["action"])

        with col_action:
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
                with st.spinner(f"'{item['name']}' 작업을 실행하고 있습니다..."):
                    result = call_gemini(
                        item["instruction"],
                        user_text,
                    )

                st.session_state.ai_result = result
                st.session_state.last_task = item["name"]
                st.session_state.history.insert(
                    0,
                    {
                        "name": item["name"],
                        "result": result,
                    },
                )
                st.session_state.history = st.session_state.history[:10]

                st.success(f"'{item['name']}' 작업이 완료되었습니다.")

            except ValueError as exc:
                st.warning(str(exc))
            except RuntimeError as exc:
                st.error(str(exc))
            except Exception as exc:
                error_text = str(exc).lower()

                if any(
                    word in error_text
                    for word in ("api_key", "api key", "unauthorized", "permission")
                ):
                    st.error(
                        "API 키가 올바르지 않거나 권한이 없습니다. "
                        "GEMINI_API_KEY 설정을 확인해 주세요."
                    )
                elif any(
                    word in error_text
                    for word in ("429", "resource_exhausted", "quota")
                ):
                    st.error(
                        "API 사용 한도에 도달했습니다. 잠시 후 다시 시도하거나 "
                        "Google AI Studio의 사용량을 확인해 주세요."
                    )
                elif any(
                    word in error_text
                    for word in ("timeout", "timed out")
                ):
                    st.error("AI 응답 시간이 초과되었습니다. 다시 시도해 주세요.")
                else:
                    st.error(
                        "AI 실행 중 오류가 발생했습니다. "
                        "API 설정과 연결 상태를 확인한 뒤 다시 시도해 주세요."
                    )
                    with st.expander("오류 상세 정보"):
                        st.code(str(exc)[:1500])


# -----------------------------
# 결과 영역
# -----------------------------
st.divider()
st.subheader("🪄 AI 실행 결과")

if st.session_state.ai_result:
    if st.session_state.last_task:
        st.caption(f"마지막 작업: {st.session_state.last_task}")

    st.text_area(
        "결과",
        value=st.session_state.ai_result,
        height=260,
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
    st.caption("아직 결과가 없습니다. 텍스트를 입력하고 단축키를 실행하세요.")


# -----------------------------
# 새 단축키 만들기
# -----------------------------
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
        help="Ctrl+Shift+문자처럼 입력하세요. 실제 키 입력은 앱 화면에서만 감지됩니다.",
    )

    new_action = st.selectbox(
        "AI 기능",
        options=list(PRESETS.keys()),
    )

    custom_instruction = st.text_area(
        "AI에게 시킬 작업",
        placeholder="예: 중학생이 이해하기 쉽게 핵심만 정리해 줘.",
        help="직접 작성 기능에서는 필수입니다. 다른 기능도 여기서 지시를 바꿀 수 있습니다.",
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
            raise ValueError("사용할 키 조합을 입력해 주세요.")

        normalized_key = normalize_shortcut(new_key_input)

        existing_keys = {
            item["key"] for item in st.session_state.shortcuts
        }
        if normalized_key in existing_keys:
            raise ValueError(
                "이미 사용 중인 단축키입니다. 다른 키 조합을 선택해 주세요."
            )

        instruction = custom_instruction.strip()
        if not instruction:
            instruction = PRESETS[new_action]

        if not instruction:
            raise ValueError(
                "직접 작성 기능을 선택했다면 AI 작업 내용을 입력해 주세요."
            )

        st.session_state.shortcuts.append(
            {
                "id": uuid.uuid4().hex[:12],
                "name": name,
                "key": normalized_key,
                "action": new_action,
                "instruction": instruction,
            }
        )
        st.success(f"'{name}' 단축키가 등록되었습니다.")
        st.rerun()

    except ValueError as exc:
        st.error(str(exc))


# -----------------------------
# 브라우저 키보드 단축키
# -----------------------------
# 키 입력은 브라우저 화면에서 감지한다.
# 브라우저/Streamlit 환경에 따라 동작이 제한될 수 있으며,
# 항상 화면의 실행 버튼으로도 실행할 수 있다.
shortcut_map = [
    {
        "key": item["key"],
        "name": item["name"],
    }
    for item in st.session_state.shortcuts
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
                const typing = tag === "textarea" ||
                    tag === "input" ||
                    (target && target.isContentEditable);

                if (typing) return;

                for (const shortcut of shortcuts) {{
                    const parts = shortcut.key.toLowerCase().split("+");
                    const key = parts[parts.length - 1];

                    const match =
                        event.ctrlKey === parts.includes("ctrl") &&
                        event.shiftKey === parts.includes("shift") &&
                        event.altKey === parts.includes("alt") &&
                        event.metaKey === parts.includes("meta") &&
                        event.key.toLowerCase() === key;

                    if (!match) continue;

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
        }} catch (e) {{
            // iframe 보안 제한이 있으면 화면 버튼을 사용한다.
        }}
    }})();
    </script>
    """,
    height=0,
)

# -----------------------------
# 최근 실행 기록
# -----------------------------
with st.expander("🕘 최근 실행 기록"):
    if st.session_state.history:
        for index, entry in enumerate(st.session_state.history, start=1):
            st.markdown(f"**{index}. {entry['name']}**")
            st.text(entry["result"][:500])
            if len(entry["result"]) > 500:
                st.caption("미리보기만 표시됩니다. 전체 결과는 위 결과 영역을 확인하세요.")
            st.divider()
    else:
        st.caption("아직 실행 기록이 없습니다.")

st.caption(
    "개인정보 보호: 입력한 텍스트는 AI 처리를 위해 Google Gemini API로 전송됩니다. "
    "비밀번호, 인증 정보 등 민감한 내용은 입력하지 마세요."
)

