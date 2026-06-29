from bs4 import BeautifulSoup       #정적인 크롤링
import requests                     #인터넷 내용을 크롤링
import pandas as pd                 #데이터 프레임으로 정리
import re                           #정규표현식
from html import unescape           #html 형식에서 깨진 글자를 복원해줌

#정제 함수
def clean_text(text):
    #text를 넣어서 clean_text를 실행했는데, text가 none이라면?
    if not text: 
        return ""       #예외처리: 값이 없으니 ""를 반환하도록
    
    #text가 있다면 (빈 값이 아니라면) 정제
    text = unescape(text.text)

    #re: 정규표현식. 텍스트를 특정 패턴으로 찾아 변형해줌
    #re.sub(패턴, 바꿀 문자, 문장): 문장에서 패턴을 찾아 바꿀 문자로 변형
    #a-zA-Z: 영문자 전체, ^: 이후로 나오는 내용을 제외, ㄱ-ㅎ가-힣: 한글 전체
    #\s (공백), \s+ (한 칸 이상의 모든 공백)
    text = re.sub(r'\s+', ' ', text.text)
    return text.strip()

#크롤링 내용을 함수화
def crawling_data(search_word):
    #크롤링 단계
    #1. '주소'를 정함 (가져올 정보가 있는 인터넷 주소)
    #2. requests.get(주소) -> 주소에 있는 html을 받아옴 (html : 인터넷에서 정보를 표현하는 파일 형식)
    #3. bs4 => 받아온 html을 '파싱'(parsing) 필요 정보 추출
    #4. bs4.select(구분자) <div></div> 와 같이 구분자 쓰인 것 모두
    #5. bs4.select_one(구분자): 구분자 쓰인 것 중 하나만
    #6. 얻어낸 정보 -> re(정규표현식)으로 '정제' or pandas로 정리 저장

    base_url = 'https://www.saramin.co.kr/zf_user/search'

    #사람인은 response와 같이 보내야하는 양식이 있음 => headers 추가
    #헤더 -> 브라우저가 서버에 무언가 요청할 때 자신의 브라우저를 밝히는 내용
    headers = {
        #요청한 브라우저의 종류는 다음 3가지입니다, 통신 언어 종류는 (accept language)를 사용합니다
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    }
    #request 보냄 -> url 답장은 response
    #headers: 웹페이지에 정보를 요청하는 브라우저에 대한 내용
    #params: 웹페이지에 이런 정보를 요청합니다~ 라는 '검색어, 검색조건' 
    #timeout: 웹페이지로부터 회신이 올 때까지 기다리는 최대치 시간
    response = requests.get(base_url, headers = headers,
                            params = {'searchword':search_word},
                            timeout = 10)

    #만약 response가 <200>이면 -> 정상
    #서버 에러 => 40~에러, 웹페이지 / 클라이언트 에러 => 50~에러, 요청자
    #response.text = html, 'html.parser' = 파서, 이를 파싱하도록 객체 생성함
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(response.text)

    #검색 결과 선별
    rows =[]
    #find: 전통적인 선택 방식
    #select: 발전된 웹 페이지 형식에 맞는 선택 방식
    #soup.select(구분자): 구분자가 들어가는 모든 내용 선택
    # soup.find_all('div', class_='item_recruit')
    for item in soup.select('div.item_recruit'):
        #1. 회사명 ('corp_name')
        #select_one(구분자): 구분자 이름을 갖는 하나만 가져오기
        corp_name = item.select_one('div.area_corp')

        #2. 채용 정보('area_job')
        job_area = item.select_one('div.area_job')

        #3. 공고 제목 ('job_tit' -> title)
        #채용 정보 속에 있는 공고 제목이니까 job_area.~
        #<div>로 시작하지 않으니 .job_tit
        #div가 아닌 job_tit라는 것을 찾아 한 개만 
        job_title = job_area.select_one('.job_tit')

        #4. 조건 ('job_condition')
        conditions = job_area.select_one('.job_condition')
        location = ''       #초기화 하고 시작하는 것
        condition1 = ''

        if conditions:
            span = conditions.select('span')
            #조건이 1개 이상 있다면~
            if len(span) > 0:
                #(형태 보고 판단)아하! 첫번째 조건은 무조건 위치군!
                location = span[0].get_text(strip = True)
            if len(span) > 1:
                #경력
                condition1 = span[1].get_text(strip=True)

        #5.직무 분야
        job_sector = job_area.select_one('.job_sector')
        job_sector = (job_sector.get_text(strip =True) if job_sector else "" )
        
        #내가 모은 정보를 '정제'함
        job_title = clean_text(job_title)
        location = clean_text(location)
        condition1 = clean_text(condition1)
        job_sector = clean_text(job_sector)
        corp_name = clean_text(corp_name)

        #rows = list, dictionary in list => for pandas
        rows.append({
            '공고 이름' : job_title,
            '회사 위치': location,
            '조건 1': condition1,
            '조건 2': job_sector,
            '회사 이름': corp_name
        })
    #최종적으로 얻어진 rows를 pd.DataFrame로 감싸 df화
    df = pd.DataFrame(rows)
    print(df)


#진입점 (이 파이썬 파일의 '실제 실행 되는 부분')
if __name__ == '__main__':
    crawling_data('인공지능')