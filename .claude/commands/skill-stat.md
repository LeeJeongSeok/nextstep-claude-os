스킬 사용 통계를 표로 출력하세요.

## 절차

아래 명령을 실행하고 결과를 그대로 출력하세요.

```bash
python3 << 'EOF'
import re
from collections import defaultdict

LOG = __import__('os').path.expanduser("~/.claude/skill-usage.log")

try:
    lines = open(LOG).readlines()
except FileNotFoundError:
    print("로그 파일이 없습니다. 스킬을 한 번 이상 호출한 뒤 다시 시도하세요.")
    exit()

if not lines:
    print("기록된 스킬 호출이 없습니다.")
    exit()

stats = defaultdict(lambda: {"count": 0, "total": 0, "min": float("inf"), "max": 0, "last": ""})

for line in lines:
    m = re.match(r"(\S+)\s*\|\s*(\S+)\s*\|\s*(\d+)s", line.strip())
    if not m:
        continue
    ts, skill, dur = m.group(1), m.group(2), int(m.group(3))
    s = stats[skill]
    s["count"] += 1
    s["total"] += dur
    s["min"] = min(s["min"], dur)
    s["max"] = max(s["max"], dur)
    s["last"] = ts

# 헤더
print()
print(f"{'스킬명':<16} {'호출횟수':>6}  {'평균':>5}  {'최소':>5}  {'최대':>5}  마지막 호출")
print("─" * 62)

for skill, s in sorted(stats.items(), key=lambda x: -x[1]["count"]):
    avg = s["total"] // s["count"]
    print(f"{skill:<16} {s['count']:>5}회  {avg:>4}s  {s['min']:>4}s  {s['max']:>4}s  {s['last']}")

print("─" * 62)
total_calls = sum(s["count"] for s in stats.values())
print(f"{'합계':<16} {total_calls:>5}회")
print()
EOF
```

출력 결과만 보여주세요. 추가 설명은 필요 없습니다.
