import streamlit as st          #파이썬 간단 프론트엔드

#웰컴벌룬~
#st.balloons()

#1. '헤더', '타이틀' 같은 큰 글씨 적용하기
# st.title("스트림릿 타이틀")
# st.header("이것은 헤더입니다.")
# st.subheader("서브헤더입니다.")


#2.'텍스트' 입력하는 방법
# 1) text: 단순한 문자열, 포매팅 없음, 고정된 형식
st.text("고정된 형식의 문자를 표시")

# 2) write: 유연한 표현이 필요할 시. 
# 입력 데이터에 따라 자동으로 적절한 형식을 지정해줘야 할 때, 데이터 프레임도 표시 가능, 문자열, 리스트 등 변수 들어갈 수 있음
color = 'red'
st.write(color)


#3.마크다운 (.md)
st.markdown("https://naver.com")
st.markdown('[naver](https://naver.com)')

#4. HTML
html_page = """
<div style="background-color:blue;padding:50px">
	<p style="color:yellow;font-size:5'px">Enjoy Streamlit!</p>
</div>
"""
#마크다운에 html 코드를 직접 삽입 -> unsafe_allow_html = true 옵션 지정해야함!
st.markdown(html_page, unsafe_allow_html=True)

#5. 반응
st.success("성공!")
st.warning("경고")
st.error("에러 발생")
st.info("정보전달")


#6. 미디어 연결
#이미지, 오디오, 유튜브 연결
#PIL (pillow 라이브러리)
from PIL import Image

#img.open(이미지가 있는 경로)
#img = Image.open("./뵤고영이.jpg")
#st.image(이미지 객체, 너비 옵션, 그림 설명)
#st.image(img, width=300, caption = 'hi!')

#open(미디어의 위치, 이 미디어로 무슨 작업?
#r (read), w(write), x(access)
#비디오 파일 소장 -> 경로로 연결
#rb -> read binary (binary = 원본 자체로 읽어오기)
# video_file = open('경로', 'rb')
# video_binary = video_file.read()        #비디오 파일을 읽어서 갖고 있다가 스트림 릿에 올려줌(아래 명령어)
#st.write(video_file) -> buffer_reader로 표시가 됨

#비디오 파일 온라인에서  st.video('영상 주소')
#st.video('https://youtu.be/HfaIcB4Ogxk?si=QkjqeCKqf_b37sJM')

#오디오 파일 연결
# audio_file = open('경로', 'rb')
# audio_binary = audio_file.read()
# st.audio(audio_binary)



#상호작용

#1. 버튼 누르기
#if 를 사용해 버튼이 눌리면 할 동작 지정
# if st.button('눌러줘요'):
#     st.balloons()

# #2. 체크박스
# if st.checkbox("체크해주세요"):
#     st.info('동의합니다.')

# #3. 라디오박스 -> 선택지가 여러 개 일때, 하나를 고르게 함 
# radio_button = st.radio('선택하세요', ['쉬기', '공부하기'])
# if radio_button == '쉬기':
#     st.success('쉬세요!')
# else:
#     st.warning('정말로?')
#     st.button('버튼을 다시 한 번 눌러주세요')

# #4. select box
# city = st.selectbox('거주지 고르세요.', ['영등포구', '강서구', '구로구'])

# #다중선택
# job = st.multiselect('희망 직무를 선택하세요', ['데이터 분석', '인공지능 개발', 'AX자동화'])




# #텍스트 입력
# #1.text_input(): 한 줄 입력 / 이름, 이메일 주소, 짧은 입력
# email = st.text_input("메일 주소를 입력하세요...", placeholder = 'abc123@gmail.com')

# if st.button('입력'):
#     st.write(email)

# #2. text_area: 여러 줄 입력 / 댓글, 설명, 피드백 같이 긴 글 입력
# st.text_area('댓글을 달아주세요', placeholder='예시) 추천합니다...')

# #nuber_input(옵션: min_value, max_value, step 셋은 모두 같은 자료형으로)
# number = st.number_input('숫자를 입력하세요.', min_value=0.00, max_value=100.00, step = 0.5)


#슬라이더
val = st.slider('값을 선택하시오', min_value= 0, max_value=10)
st.write(val)

#시간 표시

import datetime
import time
#datetiem.datetime.now(): 현재시각 표시 함수
today = st.date_input('Today is', datetime.datetime.now())
st.write(today)

#시간 입력
hour = st.time_input('the time is', datetime.time(12,30))
#현재 시간 입력
#from datetime import datetime
#hour = st.time_input('the time is', datetime.now())




#그래프 그리기
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# df = pd.read_csv('./gapminder (1).tsv', sep = '\t')
# #st.dataframe(df)

# bar = sns.barplot(df, x='country', y = 'pop')
# #plt.show() = st.pyplot()
# st.pyplot()

# #streamlit으로 바로 그림 그리기
# #streamlit이 가진 '그래프 함수' 활용, seaborn 라이브러리처럼 그리기 가능
# st.bar_chart(df, x = 'country', y='pop')



# 코드 표현
#티스토리, 노션, github pages
#json
data = {'name' : 'john', 'surname':'wick'}
st.json(data)

codes = '''
import os
path = os.path.join(origin, 'train.csv')
'''
st.code(codes, language='python')

#progress bar(UI/UX) -> tqdm
import time
# my_bar=st.progress(0)
# for v in range(100):
#     time.sleep(1)
#     my_bar.progress(v+1)

with st.spinner("기다려주세요."):
    time.sleep(10)
st.success('완료')