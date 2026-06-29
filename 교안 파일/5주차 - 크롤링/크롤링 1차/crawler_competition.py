#requests: 인터넷 요청
#bs: 정적인 웹페이지 크롤링 (상호작용이 없는 페이지, 정보 고정된 형태)
#selenium: 동적인 웹페이지 크롤링 (~~님 같이 인풋에 따라 내용이 바뀌는 형태)
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

#시간 라이브러리
import time
#진행률 표시 라이브러리 (with for문)
from tqdm import tqdm

#크롤링한 내용을 엑셀파일로 저장 위함
# xlsx -> openpyxl(파이썬으로 엑셀 컨트롤, 단점(무겁고 오류가 잘 남))
# csv -> 판다스 이용
import pandas as pd

#requests 라이브러리를 사용해 웹페이지를 읽어오기(get)
url = 'https://www.cheongwon.go.kr/portal/petition/open/view?'
response = requests.get(url)

#bs4로 웹페이지를 분해 객체 생성
#파싱 = 어떤 정보 덩어리에서 원하는 정보를 추출하는 것. 
soup = BeautifulSoup(response.text, 'html.parser')
#print(response.text)

#soup 파싱 객체가 'span'이라는 양식의 class를 찾아서 
#class - 'category'라고 적힌 내용을 category라는 변수 이름에 저장
category = soup.find_all('span', class_= 'category')
subject = soup.find_all('span', class_= 'subject')
petition = soup.find_all('span', class_= 'text')
#print(category, subject, petition)
#1차 크롤링 끝, 이후로는 가공

#크롤링한 결과물을 보기 쉬운 형태로 변환
corpus = []
for c, s, t in zip(category, subject, petition):
    corpus.append([c.text, s.text, t.text])

#2초정도 정지
time.sleep(2)

df=pd.DataFrame(corpus, columns=['카테고리', '제목', '청원내용'])
#df.to_csv(경로, 인덱스 옵션, 인코딩 옵션)
df.to_csv('./crawling_sample.csv', index = False, encoding='utf-8-sig')