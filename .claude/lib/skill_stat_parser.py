#!/usr/bin/env python3
"""
skill-stat, slack-stat 공통 로그 파싱 모듈.
사용법:
  import skill_stat_parser as p
  stats, total_calls = p.load_stats()
  print(p.format_table(stats, total_calls))
"""

import re
import os
from collections import defaultdict

LOG_PATH = os.path.expanduser("~/.claude/skill-usage.log")
LOG_PATTERN = re.compile(r"(\S+)\s*\|\s*(\S+)\s*\|\s*(\d+)s")


def load_stats(log_path: str = LOG_PATH) -> tuple[dict, int]:
    """로그 파일을 파싱해 스킬별 통계와 총 호출 수를 반환한다."""
    try:
        lines = open(log_path).readlines()
    except FileNotFoundError:
        print(f"로그 파일이 없습니다: {log_path}")
        print("스킬을 한 번 이상 호출한 뒤 다시 시도하세요.")
        raise SystemExit(1)

    if not lines:
        print("기록된 스킬 호출이 없습니다.")
        raise SystemExit(0)

    stats = defaultdict(lambda: {"count": 0, "total": 0, "min": float("inf"), "max": 0, "last": ""})

    for line in lines:
        m = LOG_PATTERN.match(line.strip())
        if not m:
            continue
        ts, skill, dur = m.group(1), m.group(2), int(m.group(3))
        s = stats[skill]
        s["count"] += 1
        s["total"] += dur
        s["min"] = min(s["min"], dur)
        s["max"] = max(s["max"], dur)
        s["last"] = ts

    total_calls = sum(s["count"] for s in stats.values())
    return dict(stats), total_calls


def format_table(stats: dict, total_calls: int) -> str:
    """스킬 통계를 터미널 출력용 표 문자열로 반환한다."""
    header = f"{'스킬명':<16} {'호출횟수':>6}  {'평균':>5}  {'최소':>5}  {'최대':>5}  마지막 호출"
    sep = "─" * 62
    rows = []

    for skill, s in sorted(stats.items(), key=lambda x: -x[1]["count"]):
        avg = s["total"] // s["count"]
        rows.append(f"{skill:<16} {s['count']:>5}회  {avg:>4}s  {s['min']:>4}s  {s['max']:>4}s  {s['last']}")

    footer = f"{'합계':<16} {total_calls:>5}회"
    return "\n".join(["", header, sep] + rows + [sep, footer, ""])


if __name__ == "__main__":
    stats, total_calls = load_stats()
    print(format_table(stats, total_calls))
