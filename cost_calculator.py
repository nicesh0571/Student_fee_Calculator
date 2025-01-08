import requests

# API 엔드포인트
url = "https://api.cnu.ac.kr/svc/oncam/pub/UnionFees?p_yy=&p_shtm=&AUTH_KEY="

# 요청 데이터
payload = {
    "p_yy": "2024",
    "p_shtm": "1"
}

# 헤더 (필요에 따라 추가)
headers = {
    "Content-Type": "application/json",
    "Authorization": "2D9BB0123ADD49A2A9504C0E63CBA7FBA6C926CC"  # API 키가 필요할 경우
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


# 기존 이벤트 딕셔너리와 인원수를 저장하는 딕셔너리는 그대로 유지
events = {
    "1학년용": {
        "새축": 10,
        "해오름제": 175,
        "성년의 날": 40
    },
    "전학년용": {
        "엠티": 1100,
        "개총": 100,
        "공대 체전": 15
    }
}

event_participants = {
    "1학년용": {
        "새축": 50,
        "해오름제": 40,
        "성년의 날": 80
    },
    "전학년용": {
        "엠티": 150,
        "개총": 100,
        "공대 체전": 30
    }
}

# 1인당 비용 계산 함수
def calculate_per_person_cost(events, participants):
    per_person_costs = {}
    for event_type, event_dict in events.items():
        per_person_costs[event_type] = {}
        for event_name, cost in event_dict.items():
            if event_name in participants.get(event_type, {}):
                num_people = participants[event_type][event_name]
                if num_people > 0:
                    per_person_costs[event_type][event_name] = cost / num_people
                else:
                    per_person_costs[event_type][event_name] = "참가자 수 없음"
            else:
                per_person_costs[event_type][event_name] = "참가자 정보 없음"
    return per_person_costs

# 1인당 비용으로 이벤트 가격 딕셔너리 업데이트
per_person_costs = calculate_per_person_cost(events, event_participants)

# 기존 합산 및 선택 함수에서 events 대신 per_person_costs 사용
def get_event_price(event_type, event_name, updated_events):
    if event_type in updated_events and event_name in updated_events[event_type]:
        return updated_events[event_type][event_name]
    else:
        return "존재하지 않는 이벤트입니다."

def sum_event_prices(updated_events, event_type, total_price):
    while True:
        print(f"\n'{event_type}' 이벤트 항목을 선택하세요:")
        for idx, event_name in enumerate(updated_events[event_type].keys(), 1):
            print(f"{idx}. {event_name}")
        
        if not updated_events[event_type]:
            print(f"'{event_type}' 이벤트 항목이 모두 선택되었습니다.")
            return total_price
        
        choice = input("번호 또는 이벤트 이름을 입력하세요 (뒤로 가려면 '뒤로'): ").strip()
        
        if choice == '뒤로':
            return total_price
        
        try:
            if choice.isdigit():
                choice = int(choice)
                selected_event = list(updated_events[event_type].keys())[choice - 1]
            else:
                selected_event = choice

            event_price = get_event_price(event_type, selected_event, updated_events)
            if isinstance(event_price, (int, float)):
                print(f"{selected_event}의 1인당 가격은 {event_price:.2f}만원입니다.")
                total_price += event_price
                del updated_events[event_type][selected_event]
            else:
                print(event_price)
        except (ValueError, IndexError):
            print("잘못된 선택입니다. 번호 또는 이벤트 이름을 다시 입력해 주세요.")

def select_and_sum_event_prices(updated_events):
    total_price = 0
    student_fee = item.get('책정금액(원)')
    student_fee = int(student_fee) / 10000   # 기본 학생 회비
    print(student_fee)
    while True:
        print("\n이벤트 유형을 선택하세요:")
        for idx, key in enumerate(updated_events.keys(), 1):
            print(f"{idx}. {key}")

        choice = input("번호 또는 이벤트 이름을 입력하세요 (종료하려면 '종료'): ").strip()
        if choice == '종료':
            print(f"\n최종 합계: {total_price:.2f}만원")
            fouryears_total_price = student_fee - (total_price * 3)
            if fouryears_total_price <= 0:
                print(f"\n이익: {-fouryears_total_price:.2f}만원")
                print("\n2학년 때 참여도를 1학년과 비슷하게, 3, 4학년 때는 참여도를 절반 정도만 하여도 이득을 볼 확률이 높습니다.")
                return
            else:
                print(f"\n손해: {fouryears_total_price:.2f}만원")
                print("손해를 볼 확률이 높습니다. 추가 선택을 고려해 보세요.")
            
            # 추가: 손익 메시지 출력 후 루프 유지
            continue

        try:
            if choice.isdigit():
                selected_type = list(updated_events.keys())[int(choice) - 1]
            else:
                selected_type = choice

            if selected_type in updated_events:
                total_price = sum_event_prices(updated_events, selected_type, total_price)
            else:
                raise ValueError

        except (ValueError, IndexError):
            print("잘못된 선택입니다. 번호 또는 이벤트 이름을 다시 입력해 주세요.")


# 1인당 비용 기반 실행
print("\n1인당 업데이트된 이벤트 가격:")
for event_type, event_dict in per_person_costs.items():
    print(f"\n{event_type}:")
    for event_name, updated_price in event_dict.items():
        if isinstance(updated_price, (int, float)):
            print(f"  {event_name}: {updated_price:.2f}만원")
        else:
            print(f"  {event_name}: {updated_price}")

select_and_sum_event_prices(per_person_costs)
