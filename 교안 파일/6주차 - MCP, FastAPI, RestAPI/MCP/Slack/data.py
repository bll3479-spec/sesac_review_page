#웹 서비스에서 사용되는 데이터의 자료형 제한
#pydantic: 웹서비스에서 자료를 주고 받을 때 자료형을 관리하는 라이브러리

from pydantic import BaseModel, Field, ValidationError

#BaseModel: '요구사항'명세서 > 데이터의 생김새 지정
#Field: 구체적으로 데이터의 크기, 예시 보여줌
#ValidationError: 에러 일으킴, DB에 잘못된 값이 들어가면 안되기에 조건을 만족하지 못했을 때 미리 에러를 발생시킴.
#                 웹의 프론트에서 데이터를 날리면 서버에서 그 데이터를 받아 동작 수행함. 그 과정에서 확인차 에러.

#BaseModel이 'User' 클래스를 관리할 것
class User(BaseModel): 
    name: str
    password: str
    age: int = Field(..., ge=0)         # ...: age가 반드시 값이 있어야 함. 필수를 의미 / ge(이상), le(이하), gt(초과), lt(미만) [greater equal / less than]
        #age 에서 자동 형변환 


try:
    valid_user = User(name='sh', password='2608', age='-10')
    print(valid_user.name, valid_user.age, type(valid_user.age))
except ValidationError as e:
    print(f'에러 발생: {e.errors()[0]['msg']}')