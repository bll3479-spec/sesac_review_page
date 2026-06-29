#프론트엔드 역할 파일

import requests

#접속할(요청할) url 정해줌. 내 컴퓨터 안에서 같이 동작하기에 127.0.0.1:8000
#포트 8000은 fastapi의 공식 포트.
url = 'http://127.0.0.1:8000/item/'

def request_item(base_url, item_id):
    #fastapi에 날아갈 내용. (post 시)
    #data = {'message':'안녕하세요'}

    url = base_url + str(item_id)
    print(f'{url}로 {item_id} 상품에 대해 질문합니다.')
    
    #requests.post(json=): json은 내가 서버에 보낼 json 형식 데이터
    response = requests.get(url)        #, json = url)
    #print(response.status_code)
    #print(response.json())
    if response.status_code == 200:
        print(f'조회 성공! {response.json().get('name')}은 {response.json().get('price')}원 입니다.')
    else: 
        print(f'오류 발생. {response.status_code}')

if __name__ == "__main__":
    #1번 아이템 (스트레스 볼) 요청하기
    url = 'http://127.0.0.1:8000/item/'
    number=input('상품 번호 : \n')
    request_item(url,number)