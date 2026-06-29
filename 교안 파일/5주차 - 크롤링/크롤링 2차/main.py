import streamlit as st
#crawling.py와 연결시키기
#from 파일명 import 파일 내 함수, 클래스 -> 해당 파일의 일부 함수/클래스만 임포트
from crawler import crawling_saramin, crawling_work24, download_to_csv
#import crawling as cr 로 정의해서 
#아래에 해당되는 부분에 cr.crawling_saramin~ 이런식으로 적용 가능

import pandas as pd

#레이아웃 (웹 페이지 생김새)
#스트림릿 웹페이지의 '헤더' 역할
st.set_page_config(page_title = "채용 공고 자동 크롤링 서비스", layout = 'wide')

st.title("채용 공고 조회 서비스")
st.write("""이 서비스는 사람인과 고용24 페이지에 검색어를 입력하여 자동으로 공고를 크롤링 하도록 만든 서비스입니다. 
         \n 크롤링 된 내용은 하단의 표에서 확인 가능하며, csv파일로 다운로드 받아 엑셀로 열어보실 수 있습니다.""")

#공고를 조회할 사이트 선택
site_select = st.radio("크롤링할 사이트 선택", ['사람인', '고용24'], horizontal = True)


#옆으로 확장되는 사이드바
# with st.sidebar:
#     st.write('사이드 확장')
#     st.button('여기!')
#     st.button('어떤 기능을!')
#     st.button('넣을래!')


#검색창 생성 -> 다단(columns) 설정

with st.expander('상세 검색 조건', expanded = True):
    col1, col2 = st.columns(2)
    with col1:
        search_text = st.text_input("검색어를 입력", placeholder= "예: 파이썬, 인공지능")
        except_text = st.text_input("제외할 검색어", placeholder="예: 야간 근무, 출장")
        max_pages = st.number_input("크롤링 페이지 수", min_value=1, max_value=30)
    with col2:
        if site_select == '사람인':
            #사람인 사이트에서만 사용 가능한 지역 코드
            loc_options = {
                "전체": None,
                "서울": "101000",
                "경기": "102000",
                "인천": "108000",
                "부산": "106000",
                "대구": "104000",
                "광주": "103000",
                "대전": "105000"
            }
            selected_location = st.multiselect('지역을 선택하세요',list(loc_options.keys()), default = ['서울'])
            #크롤링 진행할때 사용하기 위해 문자열 추출
            #지역 
            #selected_location으로 '지역명' 추출
            #loc_options가 딕셔너리이므로, loc_options[x] => x라는 '지역(키)'에 해당하는 '값'이 불러와짐
            #if조건이 붙은 이유: 예외처리. 지역명 없는 지역이면 추가 안되도록
            locations = [loc_options[x] for x in selected_location if loc_options[x]]

            #직무 검색
            cat_options = {
                "전체": None,
                "IT개발·데이터": "2",
                "경영·사무": "3",
                "마케팅·홍보": "4",
                "디자인": "9",
                "영업": "5"
            }
            selected_category = st.multiselect('직무를 선택하세요.', list(cat_options.keys()), default = ['전체'])
            category = [cat_options[x] for x in selected_category if cat_options[x]]

            #경력
            career_option = {'전체':'0', '신입': '1', '경력':'2', '신입/경력':'3'}
            selected_career = st.selectbox('경력을 선택하세요', list(career_option.keys()))
            career = career_option[selected_career]
            
            #학력
            edu_option = {'전체': '0', '고졸':'1','대졸(2,3년)':'2', '대졸(4년)': '3', '석사':'4', '박사':'5'}
            selected_edu = st.selectbox('학력을 선택하세요', list(edu_option.keys()))
            edu = edu_option[selected_edu]

        else:
            #지역, 직무, 경력, 학력
            region = st.text_input('지역 코드를 입력하세요', value='11000', help='지역 코드 알 수 없는 관계로 서울로 제한')
            occupation = st.text_input('직종 코드를 입력하세요', value='024', help = '직종 코드 제한')
           
            career_options = {"전체": "A", "신입": "N", "경력": "E", "관계없음": "Z"}
            edu_options = {"전체": "noEdu", "중졸이하": "01,02", "고졸": "03", "대졸(2~3년)": "04", "대졸(4년)": "05", "석사": "06", "박사": "07", "학력무관": "00"}
            
            career = st.selectbox('경력을 선택하세요', list(career_options.keys()))
            career = career_options[career]
            edu = st.selectbox('학력을 선택하세요', list(edu_options.keys()))
            edu = edu_options[edu]

#버튼에 들어갈 글자, use_container_width: 크기 조절 옵션(True: 최대한 늘리기), type
crawling_clicked = st.button("크롤링 시작", use_container_width= True, type = 'primary')
# #crawling_clicked -> True(버튼을 눌렀음) / False (버튼을 누르지 않았음)
# if crawling_clicked:
#     st.write('버튼을 누름')
# else:
#     st.write('버튼을 안 누름')

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
#크롤링 시행
#1. 크롤링 결과를 어떻게 받아올 것인가?
#df = 

#2. 크롤링 하는동안 어떻게 안내할 것인가?
if crawling_clicked :
    #2-1. 검색어나 필수요소가 누락된 경우 안내
    if not search_text:
        st.warning('검색어를 입력해주세요')
    #2-2. 크롤링 시행하는 동안 '기다려주세요' 라는 내용 표시
    else:
        with st.spinner(f'{site_select}에서 {search_text} 검색 결과 가져오는 중...'):
            if site_select == '사람인':
                #사람인 사이트의 내용을 크롤링하는 함수
                df = crawling_saramin(search_text = search_text, except_text = except_text, region=locations,category=category, career = career, education = edu, max_pages=max_pages)
            else:
                #고용24 사이트의 내용을 크롤링하는 함수
                df = crawling_work24(search_text =search_text , except_text=except_text , region=region, category=occupation, career = career, education = edu , max_pages= max_pages)
    st.session_state['df'] = df
#st.session_state: 
#스트림릿은 모든 상황에 랜더링을 진행하기에 크롤링 내용이 날아감
#랜더링 할때에도 남겨야할 내용(크롤링 내용, df)을 담아줌
#session_state: '딕셔너리'처럼 저장해줌
#session_state['df']로 키 지정. 이후로는 다시 df로 정의
df = st.session_state['df']
st.write(df)

#검색어 없는 화면 에러 방지용
if not df.empty:
    st.subheader('검색 결과')
    st.dataframe(df, use_container_width = True, hide_index=True)
    csv_data = download_to_csv(df)
    st.download_button(label='CSV 결과 다운로드', data=csv_data, file_name= f'crawling_results_{site_select}.csv', mime = 'text/csv')

