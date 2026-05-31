사회초년생 금융 학습 전체 진행 현황 대시보드를 출력하세요.

## 절차

### 1. 진행 데이터 읽기

아래 Python 스크립트를 실행하고 결과를 그대로 출력하세요.

```bash
python3 << 'PYEOF'
import json, os, datetime

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

TOPICS_ORDER = ["저축", "세금", "etf", "연금", "주식", "경제", "부동산", "신용"]
TOPIC_DESC = {
    "저축": "예·적금 CMA 비상금",
    "세금": "ISA 절세 연말정산",
    "etf": "인덱스 포트폴리오",
    "연금": "IRP 퇴직연금",
    "주식": "가치투자 배당",
    "경제": "금리 환율 거시경제",
    "부동산": "청약 전세 매매",
    "신용": "신용점수 대출",
}
CHECKLIST_TOTAL = {
    "저축": 5, "세금": 5, "etf": 8, "연금": 5,
    "주식": 5, "경제": 5, "부동산": 5, "신용": 5,
}

today = datetime.date.today()

print()
print("=" * 60)
print("  금융 학습 대시보드")
print(f"  {today.isoformat()}")
print("=" * 60)

# 주제별 현황 테이블
print()
print(f"  {'주제':<8} {'학습':<6} {'퀴즈':<6} {'체크리스트':<12} {'마지막 학습'}")
print("  " + "─" * 56)

total_score = 0
studied_topics = 0

for topic in TOPICS_ORDER:
    t = data.get(topic, {})

    studied = "✅" if t.get("last_studied") else "⬜"
    quiz_cnt = t.get("quiz_count", 0)
    quiz_str = f"{quiz_cnt}회" if quiz_cnt > 0 else "—"

    done_items = len(t.get("checklist_done", []))
    total_items = CHECKLIST_TOTAL[topic]
    cl_pct = int(done_items / total_items * 100)
    cl_bar = "█" * (cl_pct // 20) + "░" * (5 - cl_pct // 20)
    cl_str = f"[{cl_bar}] {cl_pct}%"

    last = t.get("last_studied", t.get("last_quiz", "—"))
    if last != "—":
        d = datetime.date.fromisoformat(last)
        days_ago = (today - d).days
        last = f"{days_ago}일 전" if days_ago > 0 else "오늘"
        studied_topics += 1

    total_score += cl_pct
    print(f"  {topic:<8} {studied:<6} {quiz_str:<6} {cl_str:<14} {last}")

print("  " + "─" * 56)

# 전체 요약
avg_score = total_score // len(TOPICS_ORDER)
big_bar = "█" * (avg_score // 10) + "░" * (10 - avg_score // 10)
total_quizzes = sum(data.get(t, {}).get("quiz_count", 0) for t in TOPICS_ORDER)

print()
print(f"  전체 진행률  [{big_bar}] {avg_score}%")
print(f"  학습 주제    {studied_topics}/{len(TOPICS_ORDER)}개 시작")
print(f"  누적 퀴즈    {total_quizzes}회")

# 다음 추천 행동
print()
print("─" * 60)
print("  다음 추천 행동")
print("─" * 60)

# 가장 오래된 학습 주제 찾기
oldest_topic = None
oldest_date = today
for topic in TOPICS_ORDER:
    t = data.get(topic, {})
    if not t.get("last_studied"):
        oldest_topic = topic
        break
    last_d = datetime.date.fromisoformat(t["last_studied"])
    if last_d < oldest_date:
        oldest_date = last_d
        oldest_topic = topic

if oldest_topic:
    print(f"  1. 학습 →  /finance-learn {oldest_topic}")
    print(f"  2. 퀴즈 →  /finance-quiz {oldest_topic}")

# 미완료 체크리스트 항목이 많은 주제
pending_topic = max(
    TOPICS_ORDER,
    key=lambda t: CHECKLIST_TOTAL[t] - len(data.get(t, {}).get("checklist_done", []))
)
pending = CHECKLIST_TOTAL[pending_topic] - len(data.get(pending_topic, {}).get("checklist_done", []))
print(f"  3. 실천 →  /finance-checklist {pending_topic}  (미완료 {pending}개)")

print()
print("  자동 학습 루프:  /finance-study")
print("=" * 60)
print()
PYEOF
```

### 2. 파일이 없는 경우

`~/.claude/finance-progress.json`이 없으면 아래를 출력하세요.

```
아직 학습 기록이 없습니다.

시작하려면:
  /finance-study       — 오늘의 학습 세션 시작 (자동 주제 선택)
  /finance-learn etf   — 특정 주제부터 시작
```

## 출력 규칙

- 스크립트 출력 결과만 그대로 표시하세요. 추가 설명 없음.
- 오류 발생 시 오류 메시지와 함께 "진행 파일을 초기화하려면 `/finance-study`를 실행하세요." 안내
