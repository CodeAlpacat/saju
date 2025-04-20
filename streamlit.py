import streamlit as st
import datetime
from main import saju_analysis
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(page_title="사주풀이 AI", page_icon="🔮", layout="centered")

# 앱 제목
st.title("🔮 사주풀이 AI 상담사")
st.markdown("---")

# 사이드바에 사용자 정보 입력 폼 구성
with st.sidebar:
    st.header("📝 개인 정보 입력")

    # 생년월일 선택 (기본값: 1996-04-07)
    birth_date = st.date_input(
        "생년월일", datetime.date(1996, 4, 7), format="YYYY-MM-DD"
    )

    # 출생 시간 선택 (기본값: 11:30)
    birth_time = st.time_input("출생 시간", datetime.time(11, 30))

    # 출생 지역 입력 (기본값: 서울)
    birth_location = st.text_input("출생 지역", value="서울")

    st.markdown("---")
    st.markdown("### ℹ️ 안내")
    st.info("정확한 사주풀이를 위해 가능한 정확한 시간을 입력해주세요.")

# 세션 상태 초기화 (대화 기록)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 사주풀이 AI 상담사입니다. 생년월일, 출생 시간, 출생 지역 정보를 바탕으로 사주에 관한 질문에 답변해 드립니다. 무엇이든 물어보세요.",
        }
    ]

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("질문을 입력하세요...")

# 사용자가 메시지를 입력하면 처리
if prompt:
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 로딩 상태 표시
    with st.chat_message("assistant"):
        with st.spinner("잠시만 기다려주세요..."):
            # 사용자 입력한 정보로 사주 분석
            formatted_birth_date = birth_date.strftime("%Y-%m-%d")
            formatted_birth_time = birth_time.strftime("%H:%M")

            try:
                # 사주 분석 함수 호출
                response = saju_analysis(
                    question=prompt,
                    birth_date=formatted_birth_date,
                    birth_time=formatted_birth_time,
                    location=birth_location,
                )

                # 응답 표시
                st.markdown(response)

                # 응답 저장
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                error_message = f"오류가 발생했습니다: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message}
                )

# 사이드바에 정보 표시
with st.sidebar:
    if st.session_state.messages:
        if st.button("대화 내용 초기화"):
            st.session_state.messages = []
            st.rerun()
