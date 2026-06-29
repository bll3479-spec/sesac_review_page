from fastapi import FastAPI
#basemodel: 서버로 들어오는 데이터 유형을 미리 정의
from pydantic import BaseModel, Field

app = FastAPI()
all_records=[]
all_workout={}

#모델을 활용해서 데이터의 송수신을 규격화 -> 서비스 에러 줄일 수 있음
#basemodel 상속 받음으로써 pydantic의 자료형 정의와 검증이 가능해짐
class HealthRecord(BaseModel):
    user_id : str = Field(...)
    height : int 
    weight : int 
    workout : bool 

#베이스 모델 만들기
# 운동에 대한 정보 모델 만들기
class WorkoutInfo(BaseModel):
    #운동종류
    wokind : str = Field(description = '운동 종류를 의미. 스쿼트, 헬스, 유산소 ...')
    #운동횟수
    wocount : int = Field(description = '운동 횟수를 의미. 얼마나 오랫동안 했는지')
    #운동강도
    wointensity : int = Field(ge =1, le = 10, description = '얼마나 강한 운동했는지, 1~10까지 직접 표현')    # 슬라이더 연계 가능   
    #greater equal 1, less equal 10

#운동 함수 만들기
# get() : 정보 출력
# post(): 운동 기록 저장

@app.post('/workout/{user_id}')
async def record_daily(user_id:str, workout:WorkoutInfo):
    #운동 기록이 저장될 것
    workout_data = workout.model_dump()
    all_workout[user_id] = workout_data
    return {'message':f'{user_id}회원님 운동 기록이 처리되었습니다.', 'saved_data' : workout_data}

@app.get('/workout')                    #관리자 모드
async def read_workout_record():
    return {'data':all_workout}


#api 설계: 
# 1. 어떤 주소 (app.get(주소 경로)/post(주소 경로)) -> 주소 정의가 우선이다
#e.g) 유저의 건강관리 기록을 어떻게 모을 것인가?
# 유저에 맵핑 되도록 할 것인가? -> id를 받고 health / recommand / my info 를 받을건지
# or 기능에 유저가 따라 붙는식으로? -> health/user_id or recommend / user_id?
# 2. 어떤 데이터? 
#e.g) app.get(주소 경로)에 개인정보가 필요하다면 
# class Personal_info() ~ 식으로


#get: 읽기 전용 / post: 쓰기 가능
@app.get('/record')                     #관리자 모드
async def read_record():
    #전체 회원에 대한 정보
    return {'data': all_records}


@app.post('/record')
async def create_record(personal_info:HealthRecord):
    #기록이 들어오면 저장
    #.model_dump(): 기록을 저장하기 위해 딕셔너리 형태로 추출
    new_data = personal_info.model_dump()
    all_records.append(new_data)
    return {'message' : f'{personal_info.user_id}님의 데이터가 성공적으로 처리되었습니다.', 'total_record': f'전체 회원 수: {len(all_records)}'}