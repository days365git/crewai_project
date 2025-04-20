import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3

import streamlit as st
import json
from crewai import Crew, Process, Task
from agents import coordinator_agent, kakao_maps_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from crew import TravelCoordinatorCrew

load_dotenv()

# Streamlit 앱 제목
st.title("🚀 여행 일정 계획 챗봇")

# 사용자 입력을 받는 영역
user_input = st.text_area(
    "여행 계획을 입력해 주세요:",
    "2025년 4월 25일부터 27일까지 서울을 출발해서 부산으로 여행을 다녀오려고 합니다. "
    "항공편, 숙소, 현지 맛집, 가볼만한 곳까지 포함해서 여행 일정을 상세히 만들어주세요. "
    "예산은 총 80만 원 이내로 잡고 있어요. "
    "혼자 가는 여행이라 너무 비싸지 않으면서 가성비 좋은 곳들로 부탁드려요."
    "추천 장소는 카카오맵으로 검색해서 링크도 함께 제공해 주세요."
)

# 여행 일정 생성 버튼
if st.button("여행 일정 생성하기"):
    with st.spinner("일정을 생성 중입니다..."):

        inputs = {
            'content': user_input
        }

        # TravelCoordinatorCrew를 통해 전체 일정 생성
        result = TravelCoordinatorCrew().crew().kickoff(inputs=inputs)

        # 카카오맵 에이전트를 통해 장소별 상세 정보 추가
        kakao_maps_result = kakao_maps_agent.kickoff(inputs=inputs)  

    st.success("여행 일정 생성 완료!")

    # 생성된 일정 결과 출력
    st.markdown("### 📝 생성된 여행 일정:")
    st.markdown(result)
    # print(result)

    # 장소별 카카오맵 링크 출력
    st.markdown("### 📍 장소별 카카오맵 링크:")
    for place in kakao_maps_result:
        st.markdown(f"- **{place['이름']}**: [카카오맵 보기]({place['링크']})")

    # try:
    #     # CrewOutput 객체에서 장소 리스트를 가져오기
    #     places = result.places  # `places`는 CrewOutput 객체의 속성으로 가정
    #     for place in places:
    #         st.markdown(f"- **{place['name']}**: [카카오맵 보기]({place['url']})")
    # except AttributeError:
    #     st.error("결과에서 장소 정보를 가져오는 중 오류가 발생했습니다.")

    # # Pydantic 모델 객체에서 데이터 추출
    # try:
    #     result_data = result.dict()  # Pydantic 모델의 dict() 메서드 사용
    #     places = result_data.get("places", [])
    #     for place in places:
    #         st.markdown(f"- **{place['name']}**: [카카오맵 보기]({place['url']})")
    # except AttributeError:
    #     st.error("CrewOutput 객체에서 데이터를 가져오는 중 오류가 발생했습니다.")


    # # CrewOutput 객체를 JSON 문자열로 변환
    # try:
    #     result_json = json.dumps(result.dict())  # Pydantic 모델이라면 dict() 사용 가능
    #     result_data = json.loads(result_json)
    #     places = result_data.get("places", [])
    #     for place in places:
    #         st.markdown(f"- **{place['name']}**: [카카오맵 보기]({place['url']})")
    # except AttributeError:
    #     st.error("CrewOutput 객체를 JSON으로 변환하는 중 오류가 발생했습니다.")
    # except json.JSONDecodeError:
    #     st.error("JSON 변환 중 오류가 발생했습니다.")