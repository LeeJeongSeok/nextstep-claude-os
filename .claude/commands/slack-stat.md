skill-stat 결과를 Slack으로 전송하세요.

## 절차

아래 명령을 순서대로 실행하세요.

### 1. 통계 생성 및 Slack 전송

```bash
python3 << 'PYEOF'
import re, os, json, subprocess
from collections import defaultdict
from datetime import datetime

# ── 설정 ──────────────────────────────────────────────────────────────────────
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
LOG = os.path.expanduser("~/.claude/skill-usage.log")
TITLE = "Claude 스킬 사용 통계"

# ── 환경변수 가드 ──────────────────────────────────────────────────────────────
if not WEBHOOK_URL:
    print("오류: SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
    print()
    print("설정 방법:")
    print("  export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/XXX/YYY/ZZZ'")
    print()
    print("Slack Incoming Webhook URL은 아래에서 생성할 수 있습니다:")
    print("  https://api.slack.com/apps → 앱 선택 → Incoming Webhooks → Add New Webhook")
    exit(1)

# ── 로그 파싱 ─────────────────────────────────────────────────────────────────
try:
    lines = open(LOG).readlines()
except FileNotFoundError:
    print("오류: 로그 파일이 없습니다 (~/.claude/skill-usage.log)")
    print("스킬을 한 번 이상 호출한 뒤 다시 시도하세요.")
    exit(1)

if not lines:
    print("기록된 스킬 호출이 없습니다.")
    exit(0)

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

# ── 표 생성 ───────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%Y-%m-%d %H:%M")
header = f"{'스킬명':<16} {'호출횟수':>6}  {'평균':>5}  {'최소':>5}  {'최대':>5}  마지막 호출"
sep    = "─" * 62
rows   = []

for skill, s in sorted(stats.items(), key=lambda x: -x[1]["count"]):
    avg = s["total"] // s["count"]
    rows.append(f"{skill:<16} {s['count']:>5}회  {avg:>4}s  {s['min']:>4}s  {s['max']:>4}s  {s['last']}")

total_calls = sum(s["count"] for s in stats.values())
footer = f"{'합계':<16} {total_calls:>5}회"

table = "\n".join(["", header, sep] + rows + [sep, footer, ""])

# ── Slack 메시지 구성 ─────────────────────────────────────────────────────────
payload = {
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f":bar_chart: {TITLE}",
                "emoji": True
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"기준 시각: *{now}*  |  총 {total_calls}회 호출"
                }
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"```{table}```"
            }
        }
    ]
}

# ── Slack 전송 ────────────────────────────────────────────────────────────────
result = subprocess.run(
    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
     "-X", "POST",
     "-H", "Content-Type: application/json",
     "-d", json.dumps(payload),
     WEBHOOK_URL],
    capture_output=True, text=True
)

http_code = result.stdout.strip()

if http_code == "200":
    print(f"Slack 전송 완료 (HTTP {http_code})")
    print(f"  채널: {WEBHOOK_URL[:50]}...")
    print(f"  기준: {now} / 총 {total_calls}회")
else:
    print(f"오류: Slack 전송 실패 (HTTP {http_code})")
    if result.stderr:
        print(f"  상세: {result.stderr}")
    exit(1)
PYEOF
```

전송 결과 메시지만 출력하세요. 추가 설명은 필요 없습니다.
