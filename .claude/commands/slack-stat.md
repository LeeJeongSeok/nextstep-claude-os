skill-stat 결과를 Slack으로 전송하세요.

## 절차

아래 명령을 실행하세요.

```bash
python3 << 'PYEOF'
import sys, os, json, subprocess
from datetime import datetime

sys.path.insert(0, "/Users/jeongseok/Desktop/nextstep/nextstep-claude-os/.claude/lib")
import skill_stat_parser as p

WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
TITLE = "Claude 스킬 사용 통계"

if not WEBHOOK_URL:
    print("오류: SLACK_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
    print()
    print("설정 방법:")
    print("  export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/XXX/YYY/ZZZ'")
    print()
    print("Slack Incoming Webhook URL은 아래에서 생성할 수 있습니다:")
    print("  https://api.slack.com/apps → 앱 선택 → Incoming Webhooks → Add New Webhook")
    sys.exit(1)

stats, total_calls = p.load_stats()
table = p.format_table(stats, total_calls)
now = datetime.now().strftime("%Y-%m-%d %H:%M")

payload = {
    "blocks": [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f":bar_chart: {TITLE}", "emoji": True}
        },
        {
            "type": "context",
            "elements": [{"type": "mrkdwn", "text": f"기준 시각: *{now}*  |  총 {total_calls}회 호출"}]
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"```{table}```"}
        }
    ]
}

result = subprocess.run(
    ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
     "-X", "POST", "-H", "Content-Type: application/json",
     "-d", json.dumps(payload), WEBHOOK_URL],
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
    sys.exit(1)
PYEOF
```

전송 결과 메시지만 출력하세요. 추가 설명은 필요 없습니다.
