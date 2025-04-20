import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 사용자 정보를 상수로 정의
USER_BIRTH_DATE = "1996-04-07"
USER_BIRTH_TIME = "11:30"
USER_BIRTH_LOCATION = "서울"


def get_openai_api_key():
    # .env 파일에 정의된 OPENAI_KEY 환경 변수 값 가져오기
    api_key = os.environ.get("OPENAI_KEY")
    if not api_key:
        raise ValueError(
            "환경 변수 OPENAI_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요."
        )
    return api_key


SYSTEM_PROMPT_SAJU = """
너는 한국 전통 사주풀이 전문가야. 다음 가이드라인에 따라 사용자의 질문에 맞는 운세를 정확하고 깊이 있게 해석해줘.

1. 역할
   - 사용자에게 친절하고 공감 어린 어조로 다가가되, 전문 지식을 바탕으로 자신감 있게 설명한다.
   - 지나치게 어려운 용어는 피하고, 꼭 필요한 전문 용어는 간단히 풀이하여 설명한다.

2. 사주 분석 기반
   - 제공된 생년월일, 출생 시간, 출생 장소를 바탕으로 사주를 구성한다.
   - 년주(年柱), 월주(月柱), 일주(日柱), 시주(時柱)의 천간·지지와 오행(목·화·토·금·수) 정보를 활용한다.

3. 질문 유형별 응답 방식
   - 구체적인 운세 질문(재물운, 건강운, 사업운, 연애운, 결혼운 등)에는 상세한 사주풀이로 응답한다.
   - '안녕하세요', '반갑습니다' 등 일반적인 인사나 명확한 운세 질문이 아닌 경우:
     * "어떤 운세를 도와드릴까요? 재물운, 건강운, 사업운, 연애운, 결혼운 등 구체적인 운세에 대해 질문해 주세요."라고 답변한다.
   - 운세와 관련 없는 질문에는 "사주풀이와 관련된 질문에 답변드릴 수 있습니다. 어떤 운세가 궁금하신가요?"라고 응답한다.

4. 질문별 맞춤형 답변
   - 사용자가 질문한 특정 운세에 집중하여 답변한다.
   - 질문과 관련된 사주 요소를 중점적으로 분석하여 구체적인 해석을 제공한다.
   - 해당 운세와 관련된 생활 조언이나 개선 방법을 함께 제시한다.

5. 응답 스타일
   - 단계별로 소제목을 사용해 깔끔하게 정리한다.
   - 길이는 300~500자 내외로 간결하게 작성한다.
   - 추가 질문이 가능함을 안내한다.

6. 주의사항
   - 제공받은 정보 외에는 절대 상상하여 추가하지 않는다.
   - 전문 용어 사용 시, 반드시 쉽게 풀이한다.
   - 질문받은 운세 외의 내용으로 답변을 확장하지 않는다.
"""


def saju_analysis(
    question: str,
    birth_date: str = USER_BIRTH_DATE,
    birth_time: str = USER_BIRTH_TIME,
    location: str = USER_BIRTH_LOCATION,
) -> str:
    """
    사주풀이를 수행하는 함수
    :param question: 사용자가 물어본 운세 질문 (예: 재물운, 건강운)
    :param birth_date: YYYY-MM-DD 형식의 생년월일 (기본값: USER_BIRTH_DATE)
    :param birth_time: HH:MM 형식의 출생 시간 (기본값: USER_BIRTH_TIME)
    :param location: 출생 지역 (기본값: USER_BIRTH_LOCATION)
    :return: GPT로부터 받은 사주풀이 텍스트
    """
    # 환경 변수에서 API 키 설정
    os.environ["OPENAI_API_KEY"] = get_openai_api_key()

    # Chat 모델 초기화
    chat = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

    # 메시지 구성
    messages = [
        SystemMessage(content=SYSTEM_PROMPT_SAJU),
        HumanMessage(
            content=(
                f"생년월일: {birth_date}\n"
                f"출생 시간: {birth_time}\n"
                f"출생 장소: {location}\n"
                f"질문: {question}\n"
                "위 정보를 바탕으로 해당 질문에 관한 사주풀이를 해주세요."
            )
        ),
    ]

    # 대화 실행
    response = chat.invoke(messages)
    return response.content


def interactive_saju_console():
    """
    대화형 사주풀이 콘솔 실행 함수
    고정된 사용자 정보를 사용하고 질문만 반복해서 받음
    """
    print("🔮 사주풀이 상담사 AI 🔮")
    print(f"기본 정보: {USER_BIRTH_DATE} {USER_BIRTH_TIME} 출생, {USER_BIRTH_LOCATION}")
    print("원하시는 질문을 입력해주세요. (종료하려면 '종료', 'quit' 또는 'exit' 입력)")

    # 대화 반복
    while True:
        question = input("\n🔮 질문: ")

        # 종료 조건
        if question.lower() in ["종료", "quit", "exit"]:
            print("사주풀이를 종료합니다. 좋은 하루 되세요!")
            break

        # 빈 질문 처리
        if not question.strip():
            print("질문을 입력해주세요.")
            continue

        # 사주 분석 및 결과 출력
        print("\n분석 중입니다...")
        try:
            result = saju_analysis(question)
            print("\n🔮 답변:")
            print(result)
            print("\n" + "-" * 60)
        except Exception as e:
            print(f"\n⚠️ 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    # 대화형 콘솔 실행
    interactive_saju_console()
