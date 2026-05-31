사회초년생 금융 학습 루프를 실행하세요. 오늘의 학습 주제를 자동 선택하고 학습 → 퀴즈 → 진행 저장까지 한 세션에 완료합니다.

## 인자

$ARGUMENTS

- 인자 없음: 가장 오래된 주제 자동 선택
- 주제 지정: `/finance-study etf` 처럼 원하는 주제 강제 선택

## 절차

### 1. 오늘의 학습 주제 결정

아래 스크립트를 실행해 오늘 학습할 주제를 결정하세요.

```bash
python3 << 'PYEOF'
import json, os, datetime, sys

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

TOPICS_ORDER = ["저축", "세금", "etf", "연금", "주식", "경제", "부동산", "신용"]
today = datetime.date.today()

forced = "$ARGUMENTS".strip().lower()
if forced and forced in TOPICS_ORDER:
    print(forced)
    sys.exit(0)

# 한 번도 학습하지 않은 주제 우선
for topic in TOPICS_ORDER:
    if not data.get(topic, {}).get("last_studied"):
        print(topic)
        sys.exit(0)

# 가장 오래전에 학습한 주제
oldest_topic = min(
    TOPICS_ORDER,
    key=lambda t: datetime.date.fromisoformat(data[t]["last_studied"])
)
print(oldest_topic)
PYEOF
```

스크립트 출력 결과를 `TODAY_TOPIC`으로 기억하세요.

---

### 2. 학습 세션 헤더 출력

```
════════════════════════════════════════
  오늘의 금융 학습: [TODAY_TOPIC]
  [오늘 날짜]
════════════════════════════════════════
```

---

### 3. 핵심 개념 복습 (5분 분량)

`TODAY_TOPIC`에 맞는 핵심 개념 5가지를 출력하세요.
(`/finance-learn`의 핵심 개념 섹션과 동일한 수준으로)

- 각 개념을 **굵은 제목** + 한 줄 설명 형식으로
- 수치 예시를 최소 2개 포함
- 오늘 시장 상황이나 최신 정보가 필요하면 WebSearch 사용

---

### 4. 오늘의 퀴즈 (5문제)

`TODAY_TOPIC` 주제로 퀴즈 5문제를 출제하세요.
(OX 2개 + 4지선다 3개, `---` 구분선 후 정답·해설)

---

### 5. 진행 저장

```bash
python3 << 'PYEOF'
import json, os, datetime

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

topic = "TODAY_TOPIC_PLACEHOLDER"  # Claude가 실제 주제로 교체
if topic not in data:
    data[topic] = {}

today = datetime.date.today().isoformat()
data[topic]["last_studied"] = today
data[topic]["quiz_count"] = data[topic].get("quiz_count", 0) + 1
data[topic]["study_count"] = data[topic].get("study_count", 0) + 1

json.dump(data, open(PATH, "w"), ensure_ascii=False, indent=2)

# 전체 현황 요약
TOPICS = ["저축", "세금", "etf", "연금", "주식", "경제", "부동산", "신용"]
studied = sum(1 for t in TOPICS if data.get(t, {}).get("last_studied"))
total_q = sum(data.get(t, {}).get("quiz_count", 0) for t in TOPICS)

print(f"\n학습 완료 저장: {topic} ({today})")
print(f"전체 진행: {studied}/8개 주제 학습 | 누적 퀴즈 {total_q}회")
PYEOF
```

위 스크립트에서 `TODAY_TOPIC_PLACEHOLDER`를 실제 `TODAY_TOPIC` 값으로 바꿔 실행하세요.

---

### 6. 세션 마무리 출력

```
════════════════════════════════════════
  학습 완료!

  오늘 학습: [TODAY_TOPIC]
  소요 시간: 약 10분

  다음 행동
  ─────────────────────────────────────
  체크리스트 실천:
    /finance-checklist [TODAY_TOPIC]

  전체 진행 현황:
    /finance-review

  다음 학습 예약 (매일 자동 실행):
    /schedule daily /finance-study

  특정 주제 집중 학습:
    /finance-learn [TODAY_TOPIC]
════════════════════════════════════════
```

---

### 7. 스케줄 안내 (최초 실행 시만)

`~/.claude/finance-progress.json`에 `scheduled` 키가 없으면 아래를 추가로 출력하세요.

```
💡 매일 자동 학습을 설정하려면:

  /schedule daily /finance-study
  → 매일 같은 시간에 자동으로 학습 세션이 실행됩니다.

  /schedule weekly /finance-review
  → 매주 1회 전체 진행 현황을 리포트합니다.
```

## 출력 규칙

- 전체 세션이 10분 내에 완료 가능한 분량으로 유지
- 핵심 개념 설명은 각 3줄 이내
- 퀴즈 해설은 각 2줄 이내
- 정보 과부하 없이 오늘 당장 실천 가능한 내용 1가지 강조
- WebSearch는 최신 금리·수치 확인이 필요할 때만 사용
