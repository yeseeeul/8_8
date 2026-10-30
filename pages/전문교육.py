import streamlit as st
import pandas as pd
from google import genai

# 페이지 기본 설정
st.set_page_config(
    page_title="노인정 전문 강사 & 교육 관리",
    page_icon="👴",
    layout="wide"
)

# 세션 상태 초기화 (강사 데이터 및 일정 데이터)
if "instructors" not in st.session_state:
    st.session_state.instructors = [
        {"이름": "김행복", "분야": "건강/실버요가", "연락처": "010-1234-5678", "특이사항": "의자 스트레칭 전문"},
        {"이름": "이스마트", "분야": "디지털/키오스크", "연락처": "010-2345-6789", "특이사항": "보이스피싱 예방 교육 가능"},
        {"이름": "박두뇌", "분야": "치매예방/보드게임", "연락처": "010-3456-7890", "특이사항": "손유희 및 미술치료 자격 보유"}
    ]

if "schedule" not in st.session_state:
    st.session_state.schedule = []

st.title("👴 노인정 주간 전문 강사 & 교육 관리 시스템")
st.caption("어르신들을 위한 매주 전문 강사 초청 일정과 만족도를 효율적으로 관리하세요.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📅 주간 교육 일정", "👨‍🏫 전문 강사 관리", "✨ AI 맞춤 교육 추천"])

# ---------------------------------------------------------
# TAB 1: 주간 교육 일정 관리
# ---------------------------------------------------------
with tab1:
    st.subheader("1. 새로운 주간 교육 일정 등록")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        edu_date = st.date_input("교육 날짜")
        edu_topic = st.text_input("교육 주제/제목", placeholder="예: 키오스크로 음식 주문하기")
    
    with col_input2:
        instructor_names = [i["이름"] + f" ({i['분야']})" for i in st.session_state.instructors]
        selected_inst = st.selectbox("초청 강사 선택", instructor_names if instructor_names else ["등록된 강사 없음"])
        attendees = st.number_input("참석 어르신 수 (명)", min_value=0, value=15)

    if st.button("일정 추가하기", type="primary"):
        if edu_topic and selected_inst != "등록된 강사 없음":
            st.session_state.schedule.append({
                "날짜": str(edu_date),
                "교육 주제": edu_topic,
                "담당 강사": selected_inst,
                "참석 인원": attendees
            })
            st.success("새로운 교육 일정이 등록되었습니다!")
            st.rerun()
        else:
            st.warning("교육 주제를 입력하고 강사를 선택해 주세요.")

    st.markdown("---")
    st.subheader("2. 전체 교육 일정 목록")
    if st.session_state.schedule:
        df_schedule = pd.DataFrame(st.session_state.schedule)
        st.dataframe(df_schedule, use_container_width=True)
    else:
        st.info("등록된 주간 교육 일정이 없습니다.")

# ---------------------------------------------------------
# TAB 2: 전문 강사 풀(Pool) 관리
# ---------------------------------------------------------
with tab2:
    st.subheader("1. 신규 전문 강사 등록")
    
    with st.form("add_instructor_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            inst_name = st.text_input("강사 이름")
            inst_category = st.selectbox("전문 분야", ["건강/운동", "디지털/스마트폰", "치매예방/인속", "교양/인문학", "기타"])
        with c2:
            inst_phone = st.text_input("연락처")
            inst_note = st.text_input("특이사항/경력")
        
        submit_inst = st.form_submit_button("강사 등록")
        if submit_inst:
            if inst_name and inst_phone:
                st.session_state.instructors.append({
                    "이름": inst_name,
                    "분야": inst_category,
                    "연락처": inst_phone,
                    "특이사항": inst_note
                })
                st.success(f"'{inst_name}' 강사님이 등록되었습니다.")
                st.rerun()
            else:
                st.error("강사 이름과 연락처를 입력해 주세요.")

    st.markdown("---")
    st.subheader("2. 등록된 전문 강사 목록")
    if st.session_state.instructors:
        df_inst = pd.DataFrame(st.session_state.instructors)
        st.dataframe(df_inst, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: AI 맞춤 교육 추천 (Gemini)
# ---------------------------------------------------------
with tab3:
    st.subheader("🤖 AI 맞춤형 교육 커리큘럼 제안")
    st.write("노인정 어르신들의 특성을 입력하시면, AI가 가장 추천하는 주간 교육 주제와 강의 구성을 제안합니다.")

    elder_info = st.text_area(
        "어르신들의 주요 연령대 및 관심사",
        placeholder="예: 70~80대 어르신이 많고, 관절 건강과 스마트폰으로 자녀들과 사진 주고받는 법에 관심이 많으십니다."
    )
    
    recommend_btn = st.button("✨ 맞춤 커리큘럼 제안받기", type="primary")

    if recommend_btn:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Secrets 설정에 'GEMINI_API_KEY'가 등록되어 있지 않습니다. Cloud 설정에서 API Key를 입력해 주세요.")
        else:
            try:
                with st.spinner("어르신 맞춤형 전문 교육안을 작성 중입니다..."):
                    client = genai.Client(api_key=api_key)
                    
                    prompt = f"""
                    당신은 노인정 및 경로당 어르신 전문 교육 기획자입니다.
                    아래 어르신들의 특성을 바탕으로, 매주 1회씩 한 달(4주) 동안 진행할 수 있는 전문 강사 초청 교육 프로그램안을 작성해 주세요.

                    [어르신 특성 및 요망사항]
                    {elder_info if elder_info.strip() else '70대 이상 어르신, 건강 및 일상 생활 유용 기능 선호'}

                    [작성 형식]
                    - 1주차: [주제] - 교육 내용 및 기대 효과
                    - 2주차: [주제] - 교육 내용 및 기대 효과
                    - 3주차: [주제] - 교육 내용 및 기대 효과
                    - 4주차: [주제] - 교육 내용 및 기대 효과
                    - 💡 **강사 초청 시 주의사항 및 팁** (1~2줄)
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=prompt,
                    )

                    st.success("맞춤 교육안 제안이 완료되었습니다!")
                    st.markdown("---")
                    st.markdown(response.text)

            except Exception as e:
                st.error(f"AI 추천 생성 중 오류가 발생했습니다: {str(e)}")
