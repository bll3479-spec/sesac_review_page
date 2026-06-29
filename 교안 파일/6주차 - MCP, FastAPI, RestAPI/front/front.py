import requests

def request_course_info(url,number):
    base_url = url + number
    response = requests.get(base_url)

    if response.status_code == 200:
        #정상 응답 받은 결과는 json 형태로 전달됨, json은 키-값 쌍이라 딕셔너리처럼 get 가능
        result = response.json()
        if 'error' in result:
            print(f'에러 발생: {result.get("error")}')
        else:
            title = result.get('title')
            prof = result.get('professor')
            print(f'강의 정보: {title} 과목 /{prof}')
    else:
        #200 으로 시작하지 않으면 대부분 오류
        #400 오류: 서버 에러
        #500 오류: 프론트 에러
        print(f'정상 코드를 수신하지 못했습니다. {response.status_code}')

#진입점
if __name__ == '__main__': 
    target_url = 'http://127.0.0.1:8000/course/'

    print('강좌를 선택하세요')
    number = input('강좌 번호 입력: \n')

    request_course_info(target_url, number)