# nextstep-claude-os

나만의 Claude Code OS — 불명확한 요구·자료·아이디어를 실행 가능한 구조와 산출물로 변환하는 개인 워크플로우 시스템.

---

## 1. 핵심 워크플로우

> 불명확한 요구·자료·아이디어를 받아서, 실행 가능한 구조와 산출물로 변환하는 워크플로우

단순히 개발하거나 문서를 작성하는 것이 아니라:

1. **해석** — 자료와 요구를 받아 의미를 파악한다
2. **구조화** — 입력을 실행 가능한 형태로 정리한다
3. **구현·작성** — 실제 산출물을 만든다
4. **기록·재사용** — 보고 가능한 결과물과 재사용 가능한 지식으로 남긴다

---

## 2. 핵심 철학

> **"먼저 작동시키고, 연결을 이해하고, 다시 쓸 수 있게 남긴다."**

- **먼저 작동시킨다** — 완벽하게 시작하기보다 작게 실행한다
- **연결을 이해한다** — 모든 업무를 입력 → 처리 → 출력 흐름으로 파악한다
- **다시 쓸 수 있게 남긴다** — 산출물과 판단 과정을 다음 업무에 재사용 가능한 형태로 기록한다

---

## 3. OS가 잘 작동하기 위해 필요한 컨텍스트

| 컨텍스트 | 핵심 질문 |
|---|---|
| **현재 상태** | 지금 무엇을 하고 있는가? |
| **완료 기준** | 무엇을 만들면 끝나는가? |
| **블로커** | 어디서 막혔는가? |
| **다음 행동** | 다음 행동은 무엇인가? |
| **재사용 자산** | 다음에 재사용할 수 있는 정보는 무엇인가? |

OS가 제대로 작동하려면 **프로젝트, 산출물, 작업 상태, 판단 기준, 연결 흐름, AI 협업 내역, 회고** 정보를 지속적으로 관리할 수 있어야 한다.

---

## 현재 구성

### 오케스트레이션 흐름

```
/task <요구사항>
      ↓
[os-orchestrator]  ← 파이프라인 조율
      ↓ 순서대로 호출
[interpret-agent] → [structure-agent] → [implement-agent] → [record-agent]
      ↓                    ↓                   ↓                  ↓
   해석 결과          태스크 구조           구현 산출물         재사용 자산
      ↓
.claude/context/current.md  ← 에이전트 간 공유 컨텍스트
```

---

### Skills (`.claude/commands/`)

#### 워크플로우 관리

| 스킬 | 사용법 | 설명 |
|---|---|---|
| `task` | `/task <요구사항>` | 새 작업 시작 → os-orchestrator 4단계 파이프라인 실행 |
| `status` | `/status` | 현재 작업 상태·진행 단계(해석/구조화/구현/기록)·블로커 출력 |
| `done` | `/done` | 작업 완료 처리 + record-agent 호출로 재사용 자산 정리 |
| `stuck` | `/stuck <블로커 내용>` | 블로커 기록 + 근본 원인 분석 + 해결 방향 2~3가지 탐색 |

#### 개발 도구

| 스킬 | 사용법 | 설명 |
|---|---|---|
| `ask` | `/ask <질문>` | 클로드 코드·개발 관련 질문에 WebSearch 팩트 체크 + 출처 제공 |
| `git-commit` | `/git-commit [메시지]` | 변경사항 분석 후 Conventional Commits 형식으로 자동 커밋 |
| `git-push` | `/git-push [--force]` | 현재 브랜치를 원격 저장소에 push (upstream 없으면 자동 설정) |
| `claude-update` | `/claude-update` | Claude Code 현재 버전 확인 → 릴리즈 노트 조회 → 최신 버전 업데이트 |

#### 통계 & 알림

| 스킬 | 사용법 | 설명 |
|---|---|---|
| `skill-stat` | `/skill-stat` | 스킬별 호출 횟수·평균/최소/최대 소요시간 통계 표 출력 |
| `slack-stat` | `/slack-stat` | skill-stat 결과를 Slack Incoming Webhook으로 전송 (환경변수 `SLACK_WEBHOOK_URL` 필요) |

#### 금융 학습 (사회초년생용)

| 스킬 | 사용법 | 설명 |
|---|---|---|
| `finance-study` | `/finance-study [주제]` | 오늘의 주제 자동 선택 → 핵심 개념 복습 → 퀴즈 5문제 → 진행 저장까지 한 세션 완료 |
| `finance-learn` | `/finance-learn <주제>` | 주제별 핵심 개념 5가지 + 유튜브 채널 추천 + 3단계 학습 로드맵 제공 |
| `finance-quiz` | `/finance-quiz <주제>` | OX 2문제 + 4지선다 3문제 출제 후 정답·해설 제공, 퀴즈 기록 저장 |
| `finance-checklist` | `/finance-checklist <주제> [번호]` | 주제별 실천 체크리스트 출력 / 번호 지정 시 완료 처리 |
| `finance-review` | `/finance-review` | 8개 주제 전체 학습·퀴즈·체크리스트 진행 현황 대시보드 출력 |

**금융 학습 주제:** `저축` · `세금` · `etf` · `연금` · `주식` · `경제` · `부동산` · `신용`

**금융 학습 빠른 시작:**
```
/finance-study          # 오늘 학습 시작 (주제 자동 선택)
/finance-review         # 전체 진행 현황 확인
/finance-checklist etf  # ETF 실천 체크리스트 확인
```

---

### Agents (`.claude/agents/`)

| 에이전트 | 단계 | 사용 도구 | 역할 |
|---|---|---|---|
| `os-orchestrator` | — | Read, Write, Edit | 4단계 파이프라인 전체 조율 (`/task` 스킬이 호출) |
| `interpret-agent` | 1단계 | Read, Write, Edit, WebSearch | 요구사항 해석 (핵심 의도·제약·모호함 명확화) |
| `structure-agent` | 2단계 | Read, Write, Edit | 구조화 (완료 기준·태스크 목록·예상 산출물 정의) |
| `implement-agent` | 3단계 | Read, Write, Edit, Bash, WebSearch | 구현·작성 (코드·문서·설정 등 실제 산출물 생성) |
| `record-agent` | 4단계 | Read, Write, Edit | 기록·재사용 (핵심 판단·패턴·회고를 다음 작업에 연결) |
| `ask-agent` | — | WebSearch, WebFetch | 개발 질문에 공식 문서 기반 출처 포함 답변 |

---

### Hooks (`.claude/hooks/`)

| 훅 파일 | 이벤트 | 동작 |
|---|---|---|
| `skill-start.sh` | `UserPromptSubmit` | `/스킬명` 패턴 감지 → 시작 시각을 `/tmp/claude_skill_{세션ID}.tmp`에 기록 |
| `skill-stop.sh` | `Stop` | 종료 시각과 비교해 소요시간 계산 → `~/.claude/skill-usage.log`에 저장 |

**로그 형식:**
```
2026-06-04T09:00:00 | finance-study  |  45s | 총 호출: 3회
```

---

### Context (`.claude/context/`)

| 파일 | 설명 |
|---|---|
| `current.md` | 현재 진행 중인 작업의 상태 (에이전트 간 공유 메모리, frontmatter로 status 관리) |

**작업 status 흐름:**
```
new → interpreting → interpreted → structuring → structured
    → implementing → implemented → recording → done
    (블로커 발생 시 → blocked)
```

---

### 데이터 파일

| 파일 | 스킬 | 설명 |
|---|---|---|
| `~/.claude/skill-usage.log` | skill-stat, slack-stat | 스킬 호출 시각·소요시간 누적 로그 |
| `~/.claude/finance-progress.json` | finance-* | 금융 학습 주제별 진행 현황 (학습일·퀴즈 횟수·체크리스트 완료 항목) |

---

### 환경변수

| 변수 | 스킬 | 설명 |
|---|---|---|
| `SLACK_WEBHOOK_URL` | slack-stat | Slack Incoming Webhook URL (없으면 설정 방법 안내 후 종료) |
