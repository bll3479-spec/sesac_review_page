#링크: https://www.musinsa.com/category/001/goods?gf=A

import requests
from bs4 import BeautifulSoup

#웹 브라우저 통신
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#시간, 판다스
import time
import pandas as pd
from tqdm import tqdm

#브라우저(크롬) 옵션
#동적으로 selenium기반 작업할 때 아래와 같은 규칙 적용해주쇼
option = Options()
option.add_argument('--no-sandbox')                         #sandbox 비활성화(보안 끄기)
option.add_argument('--disable-dev-shm-usage')              #공유 메모리 끄기
option.add_argument('--disable-gpu')                        #가속 끄기 (gpu -> 가속)
option.add_argument('--enable-unsafe-swiftshader')          #gpu 쓰지 않을 때 사용

#실제로 움직이는 webdriver
driver = webdriver.Chrome(options=option)
base_url = 'https://www.musinsa.com/categories/item/001'

#requests.get과 형식 유사!
driver.get(base_url)
time.sleep(2)

#윈도우 스크롤 내리는 스크립트 추가
#window.scrollTo(시작점, 끝점)
driver.execute_script('window.scrollTo(0,2000)')
time.sleep(2)

#창에 보이는 item 가져오기
#정적은 bs4, 동적은 selenium .find('구분자')
#html -> 웹 페이지 내용 담당, css -> 웹 페이지 디자인 담당
items = driver.find_elements(By.CSS_SELECTOR, ".sc-bSFBcf.iEkOIH" )
item_list =[]

for item in items:
    #아래의 코드 실행
    try: 
        #개별 상품에 대한 정보를 get
        #find_element(기준으로 찾아줘, a태그가 붙은 ['이름']을 가진 것 -> '이름'을 갖는 블럭을 찾아줘)
        #find_element<- 작은 범위에서 데이터를 찾아오겠다! / driver.find_elements
        a_tag = item.find_element(By.CSS_SELECTOR,"a[data-original-price]")
        
        #상품 이름
        name = a_tag.get_attribute("aria-label")
        
        #예외처리: 해당 위치에 이름을 갖고 있지 않은 경우
        #name str 처리, replace로 '상품 상세로 이동' 지우고(""로 대체), 양쪽 공백 제거
        #이후 if 활용하여 있으면 name 그대로, else의 경우 "이름 없음"으로.
        name = (str(name).replace("상품상세로 이동", "").strip() if name else "이름 없음")
        
        #브랜드 이름
        brand = a_tag.get_attribute("data-item-brand")
        #예외처리
        brand = (str(brand).strip() if brand else "브랜드 없음")

        #가격 
        price = a_tag.get_attribute("data-price")
        #예외처리
        price = (str(price).strip() if price else "가격 없음")
        
        #상세페이지
        # href: html에서 하이퍼링크 의미. 이미지/미디어로 연결되는 태그 href
        link = a_tag.get_attribute("href")
        #예외처리
        link=(str(link).strip() if link else "브랜드 없음")
        #확인
        # print(f'''name: {name},
        #       brand = {brand},
        #       price = {price},
        #       link = {link}''')
        item_list.append({
            '상품명': name,
            '브랜드': brand,
            '가격': price,
            '상품링크': link
        })

    #실행하다 '에러'가 발생하면 다음과 같이~ (예외 처리)
    except Exception as e:
        print(f'에러가 발생했습니다. :{e}')

#드라이버 종료
driver.quit()

df = pd.DataFrame(item_list) #columns=['상품명','브랜드명', '가격', '링크'])
df.to_csv('./musinsa_result.csv', index = False, encoding='utf-8-sig')