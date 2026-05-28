#!/bin/bash
# 스킬 호출 종료 시간 기록 및 로그 저장

INPUT=$(cat)
SESSION=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id','unknown'))" 2>/dev/null)

TMP="/tmp/claude_skill_${SESSION}.tmp"
[ -f "$TMP" ] || exit 0

IFS='|' read -r START SKILL < "$TMP"
END=$(date +%s)
DURATION=$((END - START))

LOG="$HOME/.claude/skill-usage.log"
touch "$LOG"

# 해당 스킬의 누적 호출 횟수 계산
COUNT=$(grep -c "| ${SKILL} |" "$LOG" 2>/dev/null || echo 0)
COUNT=$((COUNT + 1))

printf "%s | %-15s | %3ds | 총 호출: %d회\n" \
  "$(date '+%Y-%m-%dT%H:%M:%S')" "$SKILL" "$DURATION" "$COUNT" >> "$LOG"

rm -f "$TMP"
exit 0
