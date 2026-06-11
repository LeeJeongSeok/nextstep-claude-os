# 학습 인덱스 (Learning Index)

> nextstep-claude-os를 만들며 쌓은 지식을 한곳에서 찾기 위한 목차.
> "이해 → 구조 → 직접 해보기" 순서로 읽으면 좋다.

---

## 1. 이해하기 — 무엇을 만들었나

- [os-analysis.md](./os-analysis.md) — 스킬·에이전트·훅 전체 구조 분석 보고서, 개선점 우선순위
- [orchestrator-evolution.md](./orchestrator-evolution.md) — 오케스트레이터 As-Is → To-Be 진화, 설계 원칙 2가지

## 2. 직접 해보기 — 까먹지 않기 위한 실습

- [practice-quests.md](./practice-quests.md) — 6개 영역 자가 점검 과제 (★ 재현 / ★★ 변형 / ★★★ 통합)

## 3. 기준 파일 — 작업 시 참조

- [profile.md](./profile.md) — 개발자 레벨·협업 스타일
- [craft.md](./craft.md) — 코드·문서 품질 기준, 의사결정 원칙
- [history.md](./history.md) — 완료 태스크 누적 기록
- [current.md](./current.md) — 진행 중 작업의 단일 통신 채널

---

## 학습 동선 추천

1. `orchestrator-evolution.md`로 **큰 그림**(왜 위임 구조인가)을 잡는다.
2. `os-analysis.md`로 **구성요소**(스킬/에이전트/훅)와 약점을 본다.
3. `practice-quests.md`의 영역 1부터 **직접 손으로** 재현 → 변형한다.
4. 막히면 위 두 분석 문서와 실제 `.claude/` 파일을 참고로 연다.
