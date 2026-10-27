import streamlit as st
import google.generativeai as genai
from gtts import gTTS 
import io
import os

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_page_title="어르신 AI 쉬운 배움터",
    page_icon="👵",
    layout="centered"
)

# --- 어르신 맞춤형 큰 글씨 CSS 적용 ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 20px !important;
    }
    .stButton>button {
        font-size: 24px !important;
        padding: 15px 30px !important;
        border-radius: 12px !important;
        background-color: #ff9800 !important;
        color: white !important;
        width: 100% !important;
        border: none !important;
    }
    .stSelectbox label, .stTextInput label, .stTextArea label {
        font-size: 22px !important;
        font-weight: bold !important;
    }
    .mission-box {
        background-color: #fff3e0;
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #ffb74d;
        margin-bottom: 20px;
    }
    .ai-response {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #81c784;
        font-size: 22px !important;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Gemini API 설정 ---
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # 요구사항에 명시된 gemini-2.5-flash-lite 사용
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
    except Exception as e:
        st.error(f"AI 모델 설정 중 오류가 발생했습니다: {e}")
        model = None
else:
    model = None

# --- 음성 재생 함수 (TTS) ---
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='ko')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        st.warning("음성 변환 중 오류가 발생했습니다.")
        return None

# --- 메인 타이틀 ---
st.title("👵 어르신 AI 쉬운 배움터 👴")
st.write("매일 하나씩 AI와 대화하며 자연스럽게 스마트폰 사용법을 익혀보세요!")

st.divider()

# --- 탭 구성 ---
tab1, tab2 = st.tabs(["🎯 오늘의 1일 1미션", "💬 다정한 AI 말벗"])

# ==========================================
# 탭 1: 1일 1미션 기능
# ==========================================
with tab1:
    st.subheader("📋 오늘의 배움 미션")
    
    missions = [
        "미션 1: AI에게 정중하게 아침 인사 해보기",
        "미션 2: 오늘 날씨에 어울리는 옷차림 물어보기",
        "미션 3: 좋아하는 옛날 가수의 노래 추천받기",
        "미션 4: 간단하고 건강한 저녁 메뉴 추천받기",
        "미션 5: AI에게 감사 인사 전해보기"
    ]
    
    selected_mission = st.selectbox("오늘 도전할 미션을 선택하세요:", missions)
    
    st.markdown(f"""
    <div class="mission-box">
        <h3>💡 이번 미션 도우미</h3>
        <p>아래 입력창에 <b>"{selected_mission.split(': ')[1]}"</b> 내용을 참고해서 AI에게 글을 적어보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_input_mission = st.text_input("✍️ AI에게 보낼 말을 입력하세요:", placeholder="예: 안녕 AI야, 오늘 날씨에 맞는 옷을 추천해줘")
    
    if st.button("🚀 AI에게 질문 보내기 (미션 실행)", key="btn_mission"):
        if not api_key or model is None:
            st.error("🔑 API 키가 설정되지 않았습니다. Secrets 설정을 확인해주세요.")
        elif not user_input_mission.strip():
            st.warning("⚠️ 입력창에 내용을 적어주세요!")
        else:
            with st.spinner("AI가 친절하게 답장을 작성하고 있어요..."):
                try:
                    prompt = f"당신은 어르신을 다정하게 대하는 친절한 AI 조력자입니다. 쉽고 따뜻한 한국어 존댓말로, 2~3문장 이내로 짧고 명확하게 답해주세요. 질문: {user_input_mission}"
                    response = model.generate_content(prompt)
                    ai_text = response.text
                    
                    st.balloons()
                    st.success("🎉 축하합니다! 미션을 성공적으로 완료하셨습니다!")
                    
                    st.markdown("### 🤖 AI의 답변")
                    st.markdown(f'<div class="ai-response">{ai_text}</div>', unsafe_allow_html=True)
                    
                    # 음성 재생 지원
                    audio_fp = text_to_speech(ai_text)
                    if audio_fp:
                        st.write("🔊 **AI의 답변을 음성으로 들어보세요:**")
                        st.audio(audio_fp, format='audio/mp3')
                        
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

# ==========================================
# 탭 2: 다정한 AI 말벗 대화
# ==========================================
with tab2:
    st.subheader("💬 무엇이든 편하게 물어보세요")
    st.write("궁금한 점이 있거나 이야기를 나누고 싶을 때 자유롭게 글을 써주세요.")
    
    user_chat = st.text_area("✍️ 하고 싶은 말을 자유롭게 적어주세요:", height=100, placeholder="예: 요즘 무릎이 안 좋은데 좋은 운동이 있을까?")
    
    if st.button("💬 이야기 나누기", key="btn_chat"):
        if not api_key or model is None:
            st.error("🔑 API 키가 설정되지 않았습니다. Secrets 설정을 확인해주세요.")
        elif not user_chat.strip():
            st.warning("⚠️ 내용을 입력해주세요!")
        else:
            with st.spinner("AI가 정성껏 답변을 준비하고 있어요..."):
                try:
                    prompt = f"당신은 어르신들의 다정한 말벗입니다. 쉽고 친절하게, 이해하기 쉬운 단순한 문장으로 답변해 주세요. 질문: {user_chat}"
                    response = model.generate_content(prompt)
                    ai_text = response.text
                    
                    st.markdown("### 🤖 AI 말벗의 답장")
                    st.markdown(f'<div class="ai-response">{ai_text}</div>', unsafe_allow_html=True)
                    
                    # 음성 재생 지원
                    audio_fp = text_to_speech(ai_text)
                    if audio_fp:
                        st.write("🔊 **목소리로 듣기:**")
                        st.audio(audio_fp, format='audio/mp3')
                        
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")

st.divider()
st.caption("💡 팁: 스마트폰/컴퓨터 키보드의 '마이크 아이콘(음성 입력)'을 누르고 말씀하시면 글자가 자동으로 입력됩니다!")
