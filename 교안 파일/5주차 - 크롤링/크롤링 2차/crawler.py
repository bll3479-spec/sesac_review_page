#라이브러리 임포트

import requests                         #인터넷 주소(url)에 html 파일 요청
from bs4 import BeautifulSoup           #그렇게 해서 얻어온 html 파일을 예쁘게 '파싱'(필요정보 추출)
import pandas as pd                     #크롤링 df
import re                               #크롤링 정리. 문자열 정제에 사용
from io import StringIO                 #input/output

#임시 데이터 상태인 크롤링 데이터를 저장하는 코드
#buffer:임시 데이터 상태인 df를 encode한 후 결과를 반환
#함수화 이유: 배포 후 클라우드에 크롤링 결과가 존재하게 됨. 
#클라우드에서 임시파일인 buffer를 나의 컴퓨터로 다운로드 가능한 상태로 변경
def download_to_csv(df):
    buffer = StringIO()
    df.to_csv(buffer, index = False)
    return buffer.getvalue().encode('utf-8-sig')




#검색어, 제외할 검색어, 지역, 직무, 경력, 학력, 페이지 수 가 필요함
#매개변수에 입력될 자료형 '미리 안내' (:str -> 안에 들어올 자료형) 'typing'
#default 지정 = ''

#url, header, parameters -> requests.get(주소) 주소로 요청
#soup 객체로 파싱, 갖고 있다가 select(), select_one()으로 필요한 파트 추출
#처음에 초기화해놓은 rows에 append해서 최종적인 모양을 만듦
def crawling_saramin(search_text:str, except_text:str = '', region:list =None, category:list = None, career:str = "", education:str = "", max_pages:int = 1):
    #결과로 반환할 데이터 프레임의 '열 이름'과 '행' 리스트
    columns = ['이름', '위치', '조건1', '조건2', '회사이름', '링크']
    rows = []
    
    #requests 이용, 검색할 페이지에 요청 보내기
    url = "https://www.saramin.co.kr/zf_user/search"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    }
    #크롤링 페이지 
    #page : 한 페이지 검색 결과
    for page in range(1,max_pages+1):
        #파라미터 정제(검색어, 제외 검색어, 경력, 직무 등..) -> 검색 조건
        #'키'는 웹사이트에서 지정한 키
        parameters = {'searchword':search_text, 'except_read':except_text, 'comp_page':page}

        #직무
        if category :
            parameters['cat_mcd'] = category
        #위치
        if region :
            parameters['loc_mcd'] = region
        #경력
        if career:
            parameters['career_cd'] = career
        #학력
        if education:
            parameters['edu_cd'] = education

        
        try: 
            #안전성 이유로 받아줌.
            response = requests.get(url = url, headers=headers, params= parameters, timeout = 15)    #params: 조건에 대한 정보, timeout: html 반환해줄때까지 대기시간
            
            #크롤링 결과를 response로 받고, 그 안에 있는 text 파일을 'html.parser'로 파싱하는 것
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('div.item_recruit')
            for item in items:
                job_area = item.select_one('div.area_job')          #직무정보
                corp_area = item.select_one('div.area_corp')        #회사정보 가져옴

                #직무 정보가 없는 경우
                if not job_area :
                    #한 칸의 정보가 없을 때,이번만 넘어가는것.   #return X-> 강한 거부로 작용. 다른 정보들 못 가져옴
                    continue
                #그렇지 않은 경우
                job_title = job_area.select_one('.job_tit').get_text(strip=True)

                #근무조건
                condition_area = job_area.select_one('.job_condition')
                spans = condition_area.select('span')
                #근무조건 - 근무지 주소
                location = spans[0].get_text(strip=True)
                #근무조건 - 요건
                condition1 = spans[1].get_text(strip=True)
                #근무조건 - 직무 키워드 가져오기
                job_sector = item.select_one('div.job_sector')
                condition2 = job_sector.get_text(strip=True)
                #근무형태
                #condition2 = spans[-1].get_test(strip=True)
                #회사 정보
                #print(corp_area)
                #strong 사용 이유: area_corp은 이미 가져왔기에 이전에 사용한 코드에서는 가져올 게 없었음, dev tool 열면 strong 있음
                cor_name = corp_area.select_one('strong').get_text(strip=True)
                #링크 (상세공고)
                link = job_area.select_one('.job_tit').select_one('.data_layer[href]')
                real_link = 'https://www.saramin.co.kr'+link.get('href')        #링크 넘어가는 안전장치
                
                rows.append({'이름': job_title, 
                     '위치': location, 
                     '조건1': condition1, 
                     '조건2': condition2, 
                     '회사이름': cor_name, 
                     '링크': real_link})
        except Exception as e:
            print(f'에러 발생 {e}')
            break
    df = pd.DataFrame(rows)             #최종적으로 얻은 df
    #print(df)
    return df                           #return to main.py


def crawling_work24(search_text:str, except_text:str = '', region:list =None, category:list = None, career:str = "", education:str = "", max_pages:int = 1):
    #1. request
    url = 'https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    parameters ={'srcKeyword': search_text,
                 'notSrcKeyword':except_text,
                 'pageIndex':max_pages,
                 'resultCnt':10,
                 'CodeDepth1Info':region,
                 'occupation':"024",
                 'careerTypes':"",
                 'academicGbnoEdu':""}
    response = requests.get(url, headers = headers, params = parameters, timeout = 15)

    #2. soup 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    #3. 이름, 위치, 조건1, 조건2, 회사이름, 링크 soup 파싱에서 추출
    #al_left pd24 -> 회사명 -> 박스 테이블~로 해결 가능
    #link pd24 -> 조건들
    items = soup.select('div.box_table_group.gap_box08.column')
    items1 =soup.select('td.link.pd24')     #ul.emp_info_dtl 얘는 왜? 
    #=> for문 두 개로 진행

    #print(items)
    #print(items1)

    # for item in items:
        #이름:"box_chk-group"  -> cell -> t3_sb underline_hover
        #title = items.select('.cell').select_one('.t3_sb underline_hover').get_text(strip=True)
        # title = item.select_one('.cell[.t3_sb underline_hover]')

        #회사이름: "box_chk-group"-> <label> -> span -> href :cp_name underline_hover
        #1. input : value -> '|'로 구분해서 가져오기? -> no
        #2. href :cp_name underline_hover
        # cor_name = items.select('.label').select('.span').select_one('.cp_name underline_hover').get_text(strip=True)

        #링크:"cell[href]"
        # link = items.select('div.box_chk-group').select_one('div.cell[href]').get_text(strip=True)

    # for item in items1:
        
        #위치: "emp_info_dtl" -> <site> - <p>
        #site
        # site = items1.select_one('li.site').get_text(strip = True)
        
        #조건1(요건): 
        # "vline_group bar_r type2 flex_box flex_wrap" -> <"item.sm"> (경력, 학력 둘다)
        # member
        # member = items1.select_one('li.member').get_text(strip = True)
        # career = member.select('p').select_one('item.sm').get_text(strip = True)

        #조건2(직무 키워드):
        #vline_group bar_r type2 flex_box flex_wrap -> <"item.sm2, 3, 4"> (주,일,근무시간)
        # time
        # time = items1.select_one('li.time').get_text(strip = True)
        # workday = time.select('p').select_one('item.sm.2').get_text(strip = True)
        # worktime = time.select('p').select_one('item.sm.3').get_text(strip = True)

    rows = []
    for a,b in zip(items, items1):
    # #a -> 왼쪽 박스
    # #b -> 오른쪽 박스
        cells = a.select('div.cell')
        name = cells[1].get_text(strip=True)
        corp_name = cells[0].get_text(strip=True)

        #location = b.select('')
        #select(): get_text 가능
        #select_one()
        money = b.select_one('span.item.b1_sb').get_text(strip=True)
        money = re.sub(r'\s+', '', money)
        work_time = b.select_one('li.time').select('span')

        #예외처리:
        #work_time의 데이터가 불균형적이기에 일단 모든 time 셀렉, 이후로 span을 고름
        t =''
        if work_time:
            if len(work_time) > 1:
                for i in range(len(work_time)):
                    t += work_time.select('span')[i].text
            elif len(work_time)==1:
                t = work_time.select_one('span').text
            else: 
                t = ''
        else:
            t = ''
        print(t)


        # corp_name = 
        # link = 

    df = pd.DataFrame(rows)
    #print(df)
    return df

#진입점
#if __name__ == '__main__':
#     crawling_saramin('인공지능')
#      crawling_work24('AI')