사회초년생 금융 실천 체크리스트를 관리하세요.

## 인자

$ARGUMENTS

형식: `/finance-checklist <주제> [<항목번호>]`
- 항목번호 없이 호출 → 해당 주제 체크리스트 출력
- 항목번호 포함 호출 → 해당 항목을 완료 처리

## 주제별 체크리스트 정의

아래 목록이 각 주제의 전체 체크리스트입니다. (파일에 없으면 이 목록 기준으로 초기화)

```
저축:
  1. 비상금 목표 금액 설정 (생활비 3~6개월치)
  2. CMA 계좌 개설
  3. 급여일+1일 자동이체 설정
  4. 예·적금 금리 비교 앱(뱅크샐러드 등) 사용법 파악
  5. 월 저축률 30% 이상 달성

세금:
  1. ISA 계좌 개설 (연 2,000만원 비과세)
  2. 연말정산 공제 항목 전체 파악
  3. 연금저축·IRP·ISA 절세 3종 비교 학습
  4. 종합소득세 신고 대상 여부 확인
  5. 연금저축 세액공제 최대 한도 납입 실행

etf:
  1. ETF·주식·펀드 차이 개념 학습
  2. 증권사 계좌 + MTS 앱 개설
  3. 국내 ETF 종류 파악 (KODEX200, TIGER S&P500 등)
  4. KRX Academy ETF 무료 강의 수강
  5. ISA 계좌 개설
  6. 보수율·거래량 기준 ETF 선별법 학습
  7. 연금저축 계좌 개설
  8. 적립식 ETF 매수 첫 실행

연금:
  1. IRP vs 연금저축 차이 이해
  2. IRP 계좌 개설
  3. 연금저축 펀드 계좌 개설
  4. 퇴직연금 DC형 전환 가능 여부 확인
  5. 세액공제 최대 한도(연 900만원) 납입 계획 수립

주식:
  1. 재무제표 기본 3종(재무상태표·손익계산서·현금흐름표) 읽기 학습
  2. PER·PBR·ROE 개념 이해
  3. 증권사 계좌 개설 + 모의투자 경험
  4. 배당주 1종 이상 소액 매수
  5. 관심 종목 3개 1개월 이상 추적 관찰

경제:
  1. 금리와 주가·채권 관계 이해
  2. 환율 변동 요인 3가지 파악
  3. 경제 뉴스(슈카월드·한경) 매일 읽기 2주 지속
  4. GDP·CPI·기준금리 지표 해석법 학습
  5. 나만의 경제 지표 모니터링 루틴 구축

부동산:
  1. 청약통장 가입 (미가입 시 즉시 가입)
  2. 거주 지역 청약 가점·조건 파악
  3. 전세 vs 월세 vs 매매 비용 시뮬레이션
  4. 등기부등본 읽는 법 학습
  5. 관심 지역 실거래가 3개월 추적

신용:
  1. 나이스·KCB 신용점수 조회
  2. 체크카드 위주 사용 습관 형성 (신용카드 1개만 유지)
  3. 보유 대출 전체 현황 파악
  4. 소액 대출이 있으면 완전 상환 계획 수립
  5. 신용점수 올리기 전략 3가지 실행
```

## 절차

### 1. 인자 파싱

`$ARGUMENTS`를 파싱해 주제(topic)와 항목번호(item_num)를 추출하세요.
- 주제만 있으면 → 체크리스트 출력 모드
- 주제 + 숫자 있으면 → 완료 처리 모드
- 아무것도 없으면 → 사용법 안내 후 종료

### 2. 파일 읽기 및 조작

아래 Python 스크립트를 실행하세요.

**출력 모드** (항목번호 없을 때):

```bash
python3 << 'PYEOF'
import json, os, sys

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

# 주제별 체크리스트 마스터 정의 (위 목록과 동일)
CHECKLISTS = {
    "저축": ["비상금 목표 금액 설정 (생활비 3~6개월치)", "CMA 계좌 개설", "급여일+1일 자동이체 설정", "예·적금 금리 비교 앱 사용법 파악", "월 저축률 30% 이상 달성"],
    "세금": ["ISA 계좌 개설 (연 2,000만원 비과세)", "연말정산 공제 항목 전체 파악", "연금저축·IRP·ISA 절세 3종 비교 학습", "종합소득세 신고 대상 여부 확인", "연금저축 세액공제 최대 한도 납입 실행"],
    "etf": ["ETF·주식·펀드 차이 개념 학습", "증권사 계좌 + MTS 앱 개설", "국내 ETF 종류 파악", "KRX Academy ETF 무료 강의 수강", "ISA 계좌 개설", "보수율·거래량 기준 ETF 선별법 학습", "연금저축 계좌 개설", "적립식 ETF 매수 첫 실행"],
    "연금": ["IRP vs 연금저축 차이 이해", "IRP 계좌 개설", "연금저축 펀드 계좌 개설", "퇴직연금 DC형 전환 가능 여부 확인", "세액공제 최대 한도 납입 계획 수립"],
    "주식": ["재무제표 기본 3종 읽기 학습", "PER·PBR·ROE 개념 이해", "증권사 계좌 개설 + 모의투자", "배당주 1종 이상 소액 매수", "관심 종목 3개 1개월 이상 추적"],
    "경제": ["금리와 주가·채권 관계 이해", "환율 변동 요인 3가지 파악", "경제 뉴스 매일 읽기 2주 지속", "GDP·CPI·기준금리 지표 해석법 학습", "나만의 경제 지표 모니터링 루틴 구축"],
    "부동산": ["청약통장 가입 (미가입 시 즉시 가입)", "거주 지역 청약 가점·조건 파악", "전세 vs 월세 vs 매매 비용 시뮬레이션", "등기부등본 읽는 법 학습", "관심 지역 실거래가 3개월 추적"],
    "신용": ["나이스·KCB 신용점수 조회", "체크카드 위주 사용 습관 형성", "보유 대출 전체 현황 파악", "소액 대출 완전 상환 계획 수립", "신용점수 올리기 전략 3가지 실행"],
}

args = "$ARGUMENTS".strip().split()
topic = args[0].lower() if args else ""

if topic not in CHECKLISTS:
    print(f"알 수 없는 주제: {topic}")
    print("주제 목록: " + " · ".join(CHECKLISTS.keys()))
    sys.exit(0)

items = CHECKLISTS[topic]
done_set = set(data.get(topic, {}).get("checklist_done", []))
done_count = sum(1 for i in range(len(items)) if i in done_set)

print(f"\n체크리스트: {topic}  ({done_count}/{len(items)} 완료)\n")
for i, item in enumerate(items, 1):
    mark = "✅" if (i-1) in done_set else "⬜"
    print(f"  {mark} [{i}] {item}")

pct = int(done_count / len(items) * 100)
bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
print(f"\n  진행률 [{bar}] {pct}%")
print(f"\n완료 처리: /finance-checklist {topic} <번호>")
PYEOF
```

**완료 처리 모드** (항목번호 있을 때):

```bash
python3 << 'PYEOF'
import json, os, datetime

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

CHECKLISTS = {
    "저축": ["비상금 목표 금액 설정 (생활비 3~6개월치)", "CMA 계좌 개설", "급여일+1일 자동이체 설정", "예·적금 금리 비교 앱 사용법 파악", "월 저축률 30% 이상 달성"],
    "세금": ["ISA 계좌 개설 (연 2,000만원 비과세)", "연말정산 공제 항목 전체 파악", "연금저축·IRP·ISA 절세 3종 비교 학습", "종합소득세 신고 대상 여부 확인", "연금저축 세액공제 최대 한도 납입 실행"],
    "etf": ["ETF·주식·펀드 차이 개념 학습", "증권사 계좌 + MTS 앱 개설", "국내 ETF 종류 파악", "KRX Academy ETF 무료 강의 수강", "ISA 계좌 개설", "보수율·거래량 기준 ETF 선별법 학습", "연금저축 계좌 개설", "적립식 ETF 매수 첫 실행"],
    "연금": ["IRP vs 연금저축 차이 이해", "IRP 계좌 개설", "연금저축 펀드 계좌 개설", "퇴직연금 DC형 전환 가능 여부 확인", "세액공제 최대 한도 납입 계획 수립"],
    "주식": ["재무제표 기본 3종 읽기 학습", "PER·PBR·ROE 개념 이해", "증권사 계좌 개설 + 모의투자", "배당주 1종 이상 소액 매수", "관심 종목 3개 1개월 이상 추적"],
    "경제": ["금리와 주가·채권 관계 이해", "환율 변동 요인 3가지 파악", "경제 뉴스 매일 읽기 2주 지속", "GDP·CPI·기준금리 지표 해석법 학습", "나만의 경제 지표 모니터링 루틴 구축"],
    "부동산": ["청약통장 가입 (미가입 시 즉시 가입)", "거주 지역 청약 가점·조건 파악", "전세 vs 월세 vs 매매 비용 시뮬레이션", "등기부등본 읽는 법 학습", "관심 지역 실거래가 3개월 추적"],
    "신용": ["나이스·KCB 신용점수 조회", "체크카드 위주 사용 습관 형성", "보유 대출 전체 현황 파악", "소액 대출 완전 상환 계획 수립", "신용점수 올리기 전략 3가지 실행"],
}

args = "$ARGUMENTS".strip().split()
topic = args[0].lower()
item_num = int(args[1]) - 1  # 0-indexed

if topic not in data:
    data[topic] = {}
if "checklist_done" not in data[topic]:
    data[topic]["checklist_done"] = []

if item_num not in data[topic]["checklist_done"]:
    data[topic]["checklist_done"].append(item_num)
    data[topic]["checklist_done"].sort()
    data[topic]["last_checklist"] = datetime.date.today().isoformat()
    json.dump(data, open(PATH, "w"), ensure_ascii=False, indent=2)
    item_name = CHECKLISTS[topic][item_num]
    done_count = len(data[topic]["checklist_done"])
    total = len(CHECKLISTS[topic])
    print(f"✅ 완료 처리: [{args[1]}] {item_name}")
    print(f"   진행률: {done_count}/{total}")
else:
    print(f"이미 완료된 항목입니다.")
PYEOF
```

## 출력 규칙

- 스크립트 출력 결과를 그대로 표시
- 항목번호 없는 호출 후에는 `/finance-checklist <주제> <번호>` 사용법을 한 줄 안내
- 완료 처리 후에는 `/finance-review`로 전체 현황 확인 제안
