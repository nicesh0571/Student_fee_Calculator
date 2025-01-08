// 기존 이벤트와 참가자 정보를 저장하는 객체
const events = {
  "1학년용": {
    "새축": 10,
    "해오름제": 175,
    "성년의 날": 40,
  },
  "전학년용": {
    "엠티": 1100,
    "개총": 100,
    "공대 체전": 15,
  }
};

const eventParticipants = {
  "1학년용": {
    "새축": 50,
    "해오름제": 40,
    "성년의 날": 80,
  },
  "전학년용": {
    "엠티": 150,
    "개총": 100,
    "공대 체전": 30,
  }
};

// 1인당 비용 계산 함수
function calculatePerPersonCost(events, participants) {
  const perPersonCosts = {};
  for (const eventType in events) {
    perPersonCosts[eventType] = {};
    for (const eventName in events[eventType]) {
      const cost = events[eventType][eventName];
      const numPeople = participants[eventType] ? participants[eventType][eventName] : 0;
      if (numPeople > 0) {
        perPersonCosts[eventType][eventName] = cost / numPeople;
      } else {
        perPersonCosts[eventType][eventName] = "참가자 수 없음";
      }
    }
  }
  return perPersonCosts;
}

// 1인당 비용 계산 및 업데이트
const perPersonCosts = calculatePerPersonCost(events, eventParticipants);

// 이벤트 가격 가져오기 함수
function getEventPrice(eventType, eventName, updatedEvents) {
  if (updatedEvents[eventType] && updatedEvents[eventType][eventName]) {
    return updatedEvents[eventType][eventName];
  } else {
    return "존재하지 않는 이벤트입니다.";
  }
}

// 이벤트 가격 합산 함수
function sumEventPrices(updatedEvents, eventType, totalPrice) {
  while (true) {
    console.log(`\n'${eventType}' 이벤트 항목을 선택하세요:`);
    const eventNames = Object.keys(updatedEvents[eventType]);
    eventNames.forEach((eventName, idx) => {
      console.log(`${idx + 1}. ${eventName}`);
    });

    if (eventNames.length === 0) {
      console.log(`'${eventType}' 이벤트 항목이 모두 선택되었습니다.`);
      return totalPrice;
    }

    const choice = prompt("번호 또는 이벤트 이름을 입력하세요 (뒤로 가려면 '뒤로'): ").trim();

    if (choice === '뒤로') {
      return totalPrice;
    }

    try {
      let selectedEvent;
      if (isNaN(choice)) {
        selectedEvent = choice;
      } else {
        selectedEvent = eventNames[parseInt(choice) - 1];
      }

      const eventPrice = getEventPrice(eventType, selectedEvent, updatedEvents);
      if (typeof eventPrice === "number") {
        console.log(`${selectedEvent}의 1인당 가격은 ${eventPrice.toFixed(2)}만원입니다.`);
        totalPrice += eventPrice;
        delete updatedEvents[eventType][selectedEvent];
      } else {
        console.log(eventPrice);
      }
    } catch (error) {
      console.log("잘못된 선택입니다. 번호 또는 이벤트 이름을 다시 입력해 주세요.");
    }
  }
}

// 이벤트 선택 및 합산 함수
function selectAndSumEventPrices(updatedEvents) {
  let totalPrice = 0;
  const studentFee = 30; // 기본 학생 회비
  while (true) {
    console.log("\n이벤트 유형을 선택하세요:");
    Object.keys(updatedEvents).forEach((eventType, idx) => {
      console.log(`${idx + 1}. ${eventType}`);
    });

    const choice = prompt("번호 또는 이벤트 이름을 입력하세요 (종료하려면 '종료'): ").trim();
    if (choice === '종료') {
      console.log(`\n최종 합계: ${totalPrice.toFixed(2)}만원`);
      const fourYearsTotalPrice = studentFee - (totalPrice * 3);
      if (fourYearsTotalPrice <= 0) {
        console.log(`\n이익: ${(-fourYearsTotalPrice).toFixed(2)}만원`);
        console.log("\n2학년 때 참여도를 1학년과 비슷하게, 3, 4학년 때는 참여도를 절반 정도만 하여도 이득을 볼 확률이 높습니다.");
      } else {
        console.log(`\n손해: ${fourYearsTotalPrice.toFixed(2)}만원`);
        console.log("손해를 볼 확률이 높습니다. 추가 선택을 고려해 보세요.");
      }
      break;
    }

    try {
      let selectedType;
      if (isNaN(choice)) {
        selectedType = choice;
      } else {
        selectedType = Object.keys(updatedEvents)[parseInt(choice) - 1];
      }

      if (updatedEvents[selectedType]) {
        totalPrice = sumEventPrices(updatedEvents, selectedType, totalPrice);
      } else {
        throw new Error("잘못된 선택입니다.");
      }
    } catch (error) {
      console.log("잘못된 선택입니다. 번호 또는 이벤트 이름을 다시 입력해 주세요.");
    }
  }
}

// 1인당 비용 기반 실행
console.log("\n1인당 업데이트된 이벤트 가격:");
for (const eventType in perPersonCosts) {
  console.log(`\n${eventType}:`);
  for (const eventName in perPersonCosts[eventType]) {
    const updatedPrice = perPersonCosts[eventType][eventName];
    if (typeof updatedPrice === "number") {
      console.log(`  ${eventName}: ${updatedPrice.toFixed(2)}만원`);
    } else {
      console.log(`  ${eventName}: ${updatedPrice}`);
    }
  }
}

selectAndSumEventPrices(perPersonCosts);
