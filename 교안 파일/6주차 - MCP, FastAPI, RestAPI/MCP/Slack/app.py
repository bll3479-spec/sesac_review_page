#백엔드 역할 파일

from fastapi import FastAPI
#CORSMiddeleware: 다른 도메인(react)에서 이 fastAPI 서버에 들어올 수 있게 허락
#리액트: 자바 스크립트로 만들어진 프론트엔드
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel, Field 
from fastapi import Path

#fastapi로 된 '객체' 생성
#http://127.0.0.1:8000인 'app'
app = FastAPI()

#실제로 FastAPI 객체에 '외부 손님'도 들어도록 허용
app.add_middleware(
    CORSMiddleware,
    #localhost => 지금 내 컴퓨터. 3000 => react의 포트
    allow_origins = ["http://localhost:3000"],           #외부 손님이 오는 포트 이름
    allow_credentials = True,                           #쿠키, 인증 정보 전송 허용
    allow_methods = ['*'],                             #GET, POST, PUT, DELETE 등 모든 메서드 허용
    allow_headers = ["*"]                              #모든 헤더 허용
)

#@app.get('/') => app이라는 객체에 get 요청이 들어온 경우 '/'로 받아줌(최상위에서 맞이) 
#@app.~~('경로'): 경로에서만 ~~함수 실행
#http://127.0.0.1:8000이 들어오면 이 함수 실행
#@: '데코레이터'. 함수를 감싸주는 역할 for 전달
#async: 비동기. (동기식이라면 1 command가 완료될 때까지 all stop.)
@app.get('/')
async def root ():
    return {'message': 'hello, python!'}


@app.post('/')
async def chat(request : Request):
    #await: request.json() 라는 작업이 실행되는 동안 '기다림'
    #request: 클라이언트(front.py)가 보낸 데이터. 데이터를 읽는데 시간이 걸릴 수 있음(날씨 등)
    data = await request.json()

    #json{키:값}
    #json 형태로 읽어온 data가 message라는 키를 갖고 있을 것, message라는 키와 매칭되어 있는 값을 get.
    user_message = data.get('message', '')

    #응답 형태도 json으로 보냄
    return {'response':f'챗봇 응답: {user_message}를 받았습니다.'}


#이 객체를 실행시킬 때(개발버전, 실제 서버에서는 X)
#uvicorn app:app --reload
#유비콘 실행, app.py라는 파일의, app 객체를 찾아(FastAPI 객체)
#수정사항 바로 반영 --reload

#객체 실행 (실제 서버용 명령)
#--port: FastAPI 포트 번호 (8000)
#--host: 서버(나)에게 찾아올 손님의 주소 (0.0.0.0: all 환영)
#--workers: app.py가 동시에 몇 개 떠있을 것인지?
#uvicorn app:app --host 0.0.0.0 -- port 8000 --workers 1


#진입점
# if __name__ == '__main__':
#     app()

#DB에 있는 아이템(가상)
item_list = {1:{'item_id':1, 'price':3000, 'name': '스트레스 볼'}, 2:{'item_id':2, 'price':4000, 'name': '모나미 볼펜 한 다스'}}

#변수 www.naver.com/item/{바뀌는 부분}
#Field: basemodel을 미리 지정할 때 형식을 알려줌
#Path: fastapi의 함수의 매개변수로 들어올 때 형식 지정

@app.get('/item/{item_id}')
async def items(item_id : int = Path(...,ge=1)):
    #매개변수 item_id -> id를 통해 들어온 정보를 바탕으로 서버에 있는 item_list의 item_id번째를 리턴
    return item_list[item_id]