##### 기본 정보 입력 #####
import streamlit as st
# audiorecorder 패키지 추가
from audiorecorder import audiorecorder
# OpenAI 패키지 추가
import openai
# 파일 삭제를 위한 패키지 추가
import os
# 시간 정보를 위한 패키지 추가
from datetime import datetime
# TTS 패키기 추가
from gtts import gTTS
# 음원 파일 재생을 위한 패키지 추가
import base64

##### 기능 구현 함수 #####
def STT(audio):
    # 파일 저장
    filename='input.mp3'
    audio.export(filename, format="mp3")
    # 음원 파일 열기
    audio_file = open(filename, "rb")
    # Whisper 모델을 활용해 텍스트 얻기
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()
    # 파일 삭제
    os.remove(filename)
    return transcript["text"]

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

#def TTS(response):
    # gTTS 를 활용하여 음성 파일 생성
   # filename = "output.mp3"
    #tts = gTTS(text=response,lang="ko")
    #tts.save(filename)

    # 음원 파일 자동 재생생
    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="True">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md,unsafe_allow_html=True,)
    # 파일 삭제
    os.remove(filename)

##### 메인 함수 #####
def main():
    # 기본 설정
    st.set_page_config(
        page_title="음성 고양이 프로그램",
        layout="wide")

    # session state 초기화
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content": "You are a cute cat. Please answer in 25 words using the Korean."}]

    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False

    # 제목 
    st.header("음성 고양이 프로그램")
    # 구분선
    st.markdown("---")

    # 기본 설명
    with st.expander("음성고양이 프로그램에 관하여", expanded=True):
        st.write(
        """     
        - 윤주성 박시은입니다.
         - 궁금한 것을 무엇이든 물어보세요.
         - 질문의 답변을 신뢰하지 마세요.
         - 무엇이든 물어보라냥🦭
        """
        )

        st.markdown("")

    # 사이드바 생성
    with st.sidebar:

        # Open AI API 키 입력받기
        openai.api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")

        st.markdown("---")

        # GPT 모델을 선택하기 위한 라디오 버튼 생성
        model = st.radio(label="GPT 모델",options=["gpt-4", "gpt-3.5-turbo"])

        st.markdown("---")

        # 리셋 버튼 생성
        if st.button(label="초기화"):
            # 리셋 코드 
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role": "system", "content": "You are a cute cat. Please answer in 25 words using the Korean ."}]
            st.session_state["check_reset"] = True
            
    # 기능 구현 공간
    col1, col2 =  st.columns(2)
    with col1:
        # 왼쪽 영역 작성
        st.subheader("🐱질문하기🐱")
        # 음성 녹음 아이콘 추가
        audio = audiorecorder("음성 질문📞", "녹음중...")  
        if (audio.duration_seconds > 0) and (st.session_state["check_reset"]==False):
            # 음성 재생 
            st.audio(audio.export().read())
            # 음원 파일에서 텍스트 추출
            question = STT(audio)

            # 채팅을 시각화하기 위해 질문 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("user",now, question)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "user", "content": question}]

        
        textbutton = st.button("텍스트 질문✏️")
        text = st.text_input(label="텍스트 질문", placeholder="질문하기", value="")
        if textbutton :
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("user",now, text)]
            # GPT 모델에 넣을 프롬프트를 위해 질문 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "user", "content": text}]
            

    with col2:
        # 오른쪽 영역 작성
        st.subheader("🐱질문/답변🐱")
       
            
        if  (textbutton or (audio.duration_seconds > 0))  and (st.session_state["check_reset"]==False):
            # ChatGPT에게 답변 얻기
            response = ask_gpt(st.session_state["messages"], model)

            # GPT 모델에 넣을 프롬프트를 위해 답변 내용 저장
            st.session_state["messages"] = st.session_state["messages"]+ [{"role": "system", "content": response}]

            # 채팅 시각화를 위한 답변 내용 저장
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"]+ [("bot",now, response)]

            # 채팅 형식으로 시각화 하기
            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:pink;border-radius:12px;padding:8px 12px;margin-left:8px;font-family:Cute Font;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
            
            # gTTS 를 활용하여 음성 파일 생성 및 재생
         #  TTS(response)
        else:
            st.session_state["check_reset"] = False

if __name__=="__main__":
    main()
