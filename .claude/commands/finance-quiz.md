사회초년생 금융 학습 퀴즈를 출제하세요.

## 요청 주제

$ARGUMENTS

## 절차

### 1. 주제 확인

`$ARGUMENTS`가 비어 있으면 아래 안내를 출력하고 종료하세요.

```
사용법: /finance-quiz <주제>
예시:   /finance-quiz etf

주제 목록: 경제 · 부동산 · 저축 · etf · 주식 · 연금 · 세금 · 신용
```

### 2. 퀴즈 5문제 생성

아래 형식으로 `$ARGUMENTS` 주제에 맞는 퀴즈를 출력하세요.

- **OX 문제 2개** — 개념의 참/거짓을 판단
- **4지선다 객관식 3개** — 핵심 용어·수치·절차 확인

문제를 모두 출력한 뒤, 바로 아래에 `---` 구분선과 함께 정답과 해설을 이어서 출력하세요.
(사용자가 구분선 이전에서 답을 먼저 생각하도록 유도)

### 3. 출력 형식

```
## 퀴즈: [주제] — 5문제

**[OX 1]** 문제 내용
**[OX 2]** 문제 내용

**[객관식 1]** 문제 내용
  ① 보기1  ② 보기2  ③ 보기3  ④ 보기4

**[객관식 2]** 문제 내용
  ① 보기1  ② 보기2  ③ 보기3  ④ 보기4

**[객관식 3]** 문제 내용
  ① 보기1  ② 보기2  ③ 보기3  ④ 보기4

---
> 아래는 정답과 해설입니다.

**[OX 1]** O / X — 해설 (왜 그런지 한 문장)
**[OX 2]** O / X — 해설
**[객관식 1]** ③ — 해설
**[객관식 2]** ② — 해설
**[객관식 3]** ④ — 해설
```

### 4. 퀴즈 기록 저장

아래 명령을 실행해 퀴즈 기록을 `~/.claude/finance-progress.json`에 저장하세요.

```bash
python3 << 'PYEOF'
import json, os, datetime

PATH = os.path.expanduser("~/.claude/finance-progress.json")
data = json.load(open(PATH)) if os.path.exists(PATH) else {}

topic = "$ARGUMENTS".strip().lower()
if topic not in data:
    data[topic] = {}

data[topic]["last_quiz"] = datetime.date.today().isoformat()
data[topic]["quiz_count"] = data[topic].get("quiz_count", 0) + 1

json.dump(data, open(PATH, "w"), ensure_ascii=False, indent=2)
print(f"퀴즈 기록 저장 완료 · {topic} 누적 {data[topic]['quiz_count']}회")
PYEOF
```

### 5. 마무리 출력

```
/finance-checklist $ARGUMENTS  — 오늘 학습 체크리스트 확인
/finance-review                — 전체 진행 현황 대시보드
```

## 출력 규칙

- 문제는 사회초년생 수준에 맞게 실생활 예시 포함
- 수치가 있는 문제 선호 (예: "ISA 비과세 한도는 연 얼마인가?")
- 해설은 2줄 이내로 간결하게
- 정답을 먼저 노출하지 않도록 반드시 구분선 이후에 배치
