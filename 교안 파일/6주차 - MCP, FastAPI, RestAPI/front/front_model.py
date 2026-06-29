import requests

#1. 회원정보 등록
def register_personal_info(base_url):
    print('회원정보 입력을 시작합니다.')
    user_id = str(input('아이디를 입력해주세요.: \n'))
    height = int(input('신장 정보(cm)를 입력해주세요.: \n'))
    weight = int(input('체중 정보(kg)를 입력해주세요.: \n'))
    workout_intput = input('오늘 운동하셨나요? (y/n): \n').lower().strip()
    is_workout = True if workout_intput == 'y' else False                   #삼항연산

    #여기 키 값을 이렇게 적은 이유: 백엔드, 베이스 모델에서 만든 class HealthRecord에 적어줬기에
    payload = {'user_id' :user_id, 'height':height, 'weight':weight, 'workout':is_workout}
    #오류 확인: print(payload, f'{base_url}record')
    #requests에 정해진 주소로 정보 전송.
    response = requests.post(f'{base_url}record', json=payload)
    if response.status_code == 200:
        print(f'{user_id} 회원님 반갑습니다! 정보가 성공적으로 등록되었습니다.')
    else:
        print(f'등록 실패! 카운터에 문의하세요. {response.status_code}')
#2. 회원정보 조회 (관리자)
def print_personal_info(base_url):
    response = requests.get(f'{base_url}record')
    if response.status_code == 200:
        print(f'회원 정보를 열람합니다. {response.json().get("data")}')    

#3. 운동정보 등록
def register_workout_record(base_url):
    print('운동정보 입력을 시작합니다.')
    #어떤 유저가 기록했는지 알기 위해 아이디를 물어봄
    #'유저' 기록 로그인이 된 상태에서 '세션' 저장
    user_id = input('고객님의 아이디를 입력해주세요.: \n')
        #원래는 아이디가 등록된 리스트 안에 있는지 없는지 예외처리가 필요함
    wokind = input('하신 운동 종류를 입력해주세요.: \n')
    wocount = int(input('운동 횟수를 입력해주세요.: \n'))
    wointensity = int(input('운동 강도를 0~10 사이의 수로 입력해주세요.: \n'))
    
    workload = {'wokind': wokind, 'wocount': wocount, 'wointensity': wointensity}
    response = requests.post(f'{base_url}workout/{user_id}', json = workload)             #{base_url}workout!!
    if response.status_code ==200:
        print(f'{user_id}회원님의 운동정보가 성공적으로 등록되었습니다.')
    else:
        #422에러: 입력 형식이 지정해놓은 타입과 맞지 않은 경우
        #404에러: 경로 오류
        print(f'운동정보가 기록되지 않았습니다. 카운터에 문의 {response.status_code}')


#4. 운동정보 조회 (관리자)
def print_workout_record(base_url):
    response = requests.get(f'{base_url}workout')
    if response.status_code == 200:
        print(f'운동 정보를 열람합니다. {response.json().get("data")}')


#진입점
if __name__ == "__main__":
    server_url = 'http://127.0.0.1:8000/'
    #프론트만의 기능, 5. 몇 번 메뉴를 수행할 것인지?
    while True:
        print("\n========================================") 
        print(" 건강 및 운동 데이터 통합 시스템 ") 
        print("========================================")
        print(" 1. 대시보드 - 신체 정보 등록 (POST)") 
        print(" 2. 대시보드 - 전체 신체 정보 조회 (GET)") 
        print(" 3. 기록실 - 오늘의 상세 운동 등록 (POST)") 
        print(" 4. 기록실 - 전체 운동 기록 조회 (GET)") 
        print(" 5. 시스템 종료 (exit)") 
        print("========================================")

        number = input('수행할 작업 번호를 선택: 1~5').strip()

        if number == '1':                   #input -> str
            register_personal_info(server_url)
        elif number == '2':
            print_personal_info(server_url)
        elif number == '3':
            register_workout_record(server_url)
        elif number == '4':
            print_workout_record(server_url)
        elif number == '5':
            print('시스템을 종료합니다. 좋은 하루 ^^')
            break
        else:
            print(f'없는 메뉴입니다. 번호를 다시 입력하세요.')