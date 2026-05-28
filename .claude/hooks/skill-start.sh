#!/bin/bash
# 스킬 호출 시작 시간 기록

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('prompt',''))" 2>/dev/null)
SESSION=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null)

# 슬래시 커맨드(스킬) 호출 감지
if [[ "$PROMPT" =~ ^/([a-zA-Z0-9_-]+) ]]; then
  SKILL="${BASH_REMATCH[1]}"
  echo "$(date +%s)|$SKILL" > "/tmp/claude_skill_${SESSION}.tmp"
fi

exit 0
