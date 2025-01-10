import requests

# API 엔드포인트
url = "https://api.cnu.ac.kr/svc/oncam/pub/UnionFees?p_yy=&p_shtm=&AUTH_KEY="

# 요청 데이터
payload = {
    "p_yy": "2024",
    "p_shtm": "2"
}

# 헤더 (필요에 따라 추가)
headers = {
    "Content-Type": "application/json",
    "Authorization": ""  # API 키가 필요할 경우
}

# POST 요청 보내기
response = requests.post(url, json=payload, headers=headers)

# 응답 확인
if response.status_code == 200:
    data = response.json()
   # print("응답 성공:", data)

    result = data.get("RESULT", [])
    target_department = "컴퓨터융합학부"
    
    # "컴퓨터융합학부" 데이터 검색
    filtered_data = [item for item in result if item.get("학과명") == target_department]
    
    if filtered_data:
        print(f"{target_department} 관련 데이터:")
        for item in filtered_data:
            print(f"연도: {item.get('연도')}, 학기: {item.get('학기')}, 단과대명: {item.get('단과대명')}, "
                  f"학과명: {item.get('학과명')}, 책정금액(원): {item.get('책정금액(원)')}")
    else:
        print(f"{target_department} 데이터가 없습니다.")
    
else:
    print("오류 발생:", response.status_code, response.text)
