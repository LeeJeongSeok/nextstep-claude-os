# nextstep-claude-os 스킬·에이전트 구조 분석 보고서

> 작성일: 2026-05-28  
> 분석 대상: `.claude/commands/` (8개), `.claude/agents/` (6개), `.claude/hooks/` (2개), `settings.json`

---

## 1. 현황 파악

### 1-1. 스킬(Slash Commands) 목록

| 스킬명 | 파일 | 입력($ARGUMENTS) | 핵심 역할 | 에이전트 위임 |
|--------|------|-----------------|-----------|--------------|
| `ask` | `ask.md` | 질문 텍스트 | 개발 질문 WebSearch 답변 | 없음 (직접 실행) |
| `done` | `done.md` | 없음 | 현재 작업 완료 처리 | `record-agent` |
| `git-commit` | `git-commit.md` | 커밋 메시지(선택) | git 변경사항 분석·커밋 | 없음 (직접 실행) |
| `skill-stat` | `skill-stat.md` | 없음 | 스킬 사용 통계 터미널 출력 | 없음 (python3 인라인) |
| `slack-stat` | `slack-stat.md` | 없음 | 스킬 통계를 Slack 전송 | 없음 (python3 인라인) |
| `status` | `status.md` | 없음 | 현재 작업 상태 조회 | 없음 (직접 읽기) |
| `stuck` | `stuck.md` | 블로커 내용 | 블로커 기록·해결 방향 탐색 | 없음 (직접 실행) |
| `task` | `task.md` | 요구사항 | 새 작업 시작 → 4단계 워크플로우 | `os-orchestrator` |

### 1-2. 에이전트(Agents) 목록

| 에이전트명 | 파일 | 사용 도구 | 담당 단계 | 호출자 |
|-----------|------|----------|---------|--------|
| `os-orchestrator` | `os-orchestrator.md` | Read, Write, Edit | 파이프라인 전체 조율 | `/task` 스킬 |
| `interpret-agent` | `interpret-agent.md` | Read, Write, Edit, WebSearch | 1단계: 요구사항 해석 | `os-orchestrator` |
| `structure-agent` | `structure-agent.md` | Read, Write, Edit | 2단계: 구조화 | `os-orchestrator` |
| `implement-agent` | `implement-agent.md` | Read, Write, Edit, Bash, WebSearch | 3단계: 구현 | `os-orchestrator` |
| `record-agent` | `record-agent.md` | Read, Write, Edit | 4단계: 기록 | `os-orchestrator`, `/done` 스킬 |
| `ask-agent` | `ask-agent.md` | WebSearch, WebFetch | 질문 답변 | (직접 참조 없음) |

### 1-3. 훅(Hooks) 분석

| 파일 | 트리거 훅 | 역할 |
|------|----------|------|
| `skill-start.sh` | `UserPromptSubmit` | 슬래시 커맨드 감지 시 시작 시각(Unix timestamp) + 스킬명을 `/tmp/claude_skill_{session}.tmp`에 저장 |
| `skill-stop.sh` | `Stop` | tmp 파일을 읽어 실행 시간 계산 후 `~/.claude/skill-usage.log`에 기록 |

**로그 포맷**: `{ISO8601} | {skill명:<15} | {duration:3}s | 총 호출: {n}회`

### 1-4. 호출 관계도

```
사용자
  │
  ├─ /task <요구사항>
  │     └─ os-orchestrator
  │           ├─ interpret-agent   (1단계)
  │           ├─ structure-agent   (2단계)
  │           ├─ implement-agent   (3단계)
  │           └─ record-agent      (4단계)
  │
  ├─ /done
  │     └─ record-agent
  │
  ├─ /status      → current.md 직접 읽기
  ├─ /stuck       → current.md 직접 수정
  ├─ /git-commit  → git 직접 실행
  ├─ /ask         → WebSearch 직접 실행
  ├─ /skill-stat  → python3 인라인 스크립트
  └─ /slack-stat  → python3 인라인 스크립트 + curl
```

---

## 2. 개선점 분석

### 관점 A: 구조적 일관성

#### A-1. `ask` 스킬과 `ask-agent` 의 단절 [HIGH]

- **문제**: `ask.md` 스킬은 에이전트를 위임하지 않고 직접 WebSearch를 수행하는 반면, `ask-agent.md`가 별도로 존재함. `ask.md`에는 `ask-agent`를 호출하는 흐름이 없어 `ask-agent`가 사실상 사용되지 않는 상태.
- **개선안**: `ask.md`에서 `ask-agent`를 호출하도록 수정하거나, `ask-agent.md`를 제거해 중복을 없앤다.

#### A-2. 스킬 파일의 포맷 불일치 [MEDIUM]

- **문제**: 일부 스킬은 frontmatter 없이 순수 텍스트로 시작 (`ask.md`, `skill-stat.md`, `slack-stat.md` 등), 에이전트 파일은 모두 YAML frontmatter(`name`, `description`, `tools`)를 가짐. 스킬 파일에도 메타데이터 표준이 없어 자동 파싱이나 문서화가 어렵다.
- **개선안**: 스킬 파일에도 최소한의 frontmatter 도입 — `name`, `description`, `arguments` 항목 추가.

#### A-3. `done.md`에서 `record-agent` 호출 vs `os-orchestrator`의 4단계 내 `record-agent` 호출 중복 [MEDIUM]

- **문제**: `record-agent`가 `/done` 스킬과 `os-orchestrator` 양쪽에서 호출될 수 있어, 워크플로우 중간에 사용자가 `/done`을 실행하면 미완성 상태에서 기록이 완료될 수 있다.
- **개선안**: `record-agent` 호출 전 `status`가 `implemented` 상태인지 검증하는 가드 로직 추가.

---

### 관점 B: 기능 완결성

#### B-1. `update-config` 스킬 미존재 [HIGH]

- **문제**: CLAUDE.md 기준 available skills 목록에 `update-config`가 포함되어 있지만, `.claude/commands/`에 해당 파일이 없다. 실제로 `/update-config`를 호출하면 동작하지 않는다.
- **개선안**: `update-config.md` 스킬 파일 신규 작성 (settings.json, settings.local.json 설정 변경 기능).

#### B-2. 태스크 관리 기능 없음 [MEDIUM]

- **문제**: current.md 단일 파일로 작업 상태를 관리하므로 동시에 하나의 작업만 추적 가능. 여러 작업을 병렬로 진행하거나 히스토리를 보려면 방법이 없다.
- **개선안**: `current.md` 외에 `history/` 디렉터리를 도입해 완료된 작업을 `{id}.md`로 아카이빙하고, `/task-list` 스킬로 히스토리 조회 기능 추가.

#### B-3. 훅이 `Stop` 이벤트만 사용 → 비정상 종료 시 로그 유실 [MEDIUM]

- **문제**: `skill-stop.sh`는 `Stop` 훅에 연결되어 있어 Claude Code가 정상 종료될 때만 실행된다. 강제 종료(Ctrl+C, 크래시)의 경우 `/tmp` 임시 파일은 남아 있지만 로그에 기록되지 않는다.
- **개선안**: `skill-start.sh`에서 시작 시각을 tmp 파일뿐 아니라 로그에 `STARTED` 상태로도 기록하고, `skill-stop.sh`에서 해당 항목을 `COMPLETED`로 업데이트하는 방식으로 변경.

#### B-4. `/stuck` 스킬의 자동 복구 후 status 전환 로직 취약 [LOW]

- **문제**: `stuck.md`는 status를 `blocked`로 바꾼 뒤 "이전 status로 되돌린다"고 명시하지만, "이전 status"를 파일에서 직접 추적하지 않는다. 에이전트가 임의로 추론해야 하는 모호함이 있다.
- **개선안**: frontmatter에 `prev_status` 필드를 추가하거나, blocked 진입 전 상태를 `## 블로커` 섹션에 함께 기록하도록 형식 강제.

---

### 관점 C: 재사용성

#### C-1. `skill-stat.md`와 `slack-stat.md`의 로그 파싱 로직 중복 [HIGH]

- **문제**: 동일한 Python 파싱 코드(정규식, defaultdict 통계 집계)가 두 파일에 완전히 복사되어 있다. 로그 포맷이 변경되면 두 파일을 모두 수정해야 한다.
- **개선안**: 공통 파싱 로직을 `.claude/lib/skill_stat_parser.py`로 추출하고 두 스킬 모두 `python3 .claude/lib/skill_stat_parser.py`를 호출하는 방식으로 리팩터링.

#### C-2. 에이전트에 공통 컨텍스트 파일 읽기 패턴 반복 [MEDIUM]

- **문제**: `interpret-agent`, `structure-agent`, `implement-agent`, `record-agent` 모두 첫 번째 작업으로 `.claude/context/current.md`를 읽고 status를 업데이트하는 동일한 패턴을 가진다. 이 패턴이 각 에이전트 프롬프트에 텍스트로 중복 기재되어 있다.
- **개선안**: `os-orchestrator`가 각 에이전트를 호출하기 전에 현재 context 상태를 인자로 전달하거나, 공통 프리앰블을 별도 파일로 추출해 include 방식 사용.

#### C-3. 외부 채널 전송 패턴 일반화 가능 [LOW]

- **문제**: `slack-stat.md`는 특정 외부 채널(Slack)로 전송하는 패턴을 구현했는데, 동일한 패턴이 다른 통계(task-stat, git-stat 등)에도 필요할 수 있다.
- **개선안**: "데이터 생성 → 외부 채널 전송" 패턴을 템플릿화해 신규 스킬 작성 가이드로 문서화.

---

### 관점 D: 운영 안정성

#### D-1. 훅에서 `bash .claude/hooks/skill-start.sh` 상대 경로 사용 [HIGH]

- **문제**: `settings.json`에 훅 커맨드가 `bash .claude/hooks/skill-start.sh`로 상대 경로로 등록되어 있다. Claude Code의 실행 디렉터리가 프로젝트 루트가 아닐 경우 훅이 동작하지 않는다.
- **개선안**: 절대 경로 또는 `${CLAUDE_PROJECT_ROOT}` 형태의 환경변수 기반 경로로 변경.

#### D-2. `os-orchestrator`에 에이전트 실패 처리 메커니즘 부재 [HIGH]

- **문제**: `os-orchestrator.md`는 각 에이전트를 순서대로 호출하지만, 에이전트가 실패하거나 status 업데이트를 하지 않을 경우의 재시도·중단 로직이 없다.
- **개선안**: 각 단계 완료 후 context 파일의 status를 검증하는 assert 단계를 오케스트레이터에 추가. 예상 status가 아니면 `/stuck`에 자동 기록.

#### D-3. `skill-stop.sh` 로그 파싱 정규식과 `skill-stat.md` 파싱 정규식 불일치 위험 [MEDIUM]

- **문제**: `skill-stop.sh`의 로그 출력 포맷 (`printf "%s | %-15s | %3ds | 총 호출: %d회\n"`)과 `skill-stat.md`/`slack-stat.md`의 파싱 정규식 (`r"(\S+)\s*\|\s*(\S+)\s*\|\s*(\d+)s"`)이 각각 독립적으로 정의되어 있어, 한쪽이 변경되면 다른 쪽이 깨진다.
- **개선안**: 로그 포맷을 단일 상수로 정의하거나, 파싱 테스트 케이스를 추가.

#### D-4. `settings.local.json`의 allow 목록 과도하게 좁음 [LOW]

- **문제**: `Bash(git commit -m ' *)`처럼 따옴표 패턴으로 허용 범위를 제한했지만, 실제 커밋 메시지에 다양한 특수문자가 포함될 경우 허용 실패가 발생할 수 있다.
- **개선안**: git 관련 허용 패턴을 `Bash(git *)` 수준으로 단순화하거나, 별도 권한 그룹으로 분리.

---

## 3. 개선점 우선순위 요약

| 우선순위 | 항목 | 예상 영향 |
|---------|------|---------|
| HIGH | A-1: ask 스킬 ↔ ask-agent 단절 | ask-agent 사문화 |
| HIGH | B-1: update-config 스킬 미존재 | 호출 시 오류 |
| HIGH | C-1: 로그 파싱 코드 중복 | 유지보수 부담 |
| HIGH | D-1: 훅 상대 경로 | 훅 미동작 위험 |
| HIGH | D-2: 오케스트레이터 실패 처리 부재 | 파이프라인 중단 시 복구 불가 |
| MEDIUM | A-2: 스킬 파일 포맷 불일치 | 자동화·문서화 어려움 |
| MEDIUM | A-3: done/record-agent 이중 호출 | 미완성 기록 위험 |
| MEDIUM | B-2: 단일 작업만 추적 가능 | 병렬 작업 불가 |
| MEDIUM | B-3: 비정상 종료 시 로그 유실 | 통계 부정확 |
| MEDIUM | C-2: 에이전트 공통 패턴 중복 | 프롬프트 비대화 |
| MEDIUM | D-3: 로그 포맷·파싱 정규식 불일치 위험 | 통계 파싱 오류 |
| LOW | B-4: stuck 이전 status 모호 | 에이전트 오판 가능 |
| LOW | C-3: 외부 채널 전송 패턴 미일반화 | 확장성 제한 |
| LOW | D-4: settings.local.json 허용 패턴 | 간헐적 권한 오류 |

---

## 4. 권장 즉시 개선 항목 (Quick Win)

1. **`ask.md` → `ask-agent` 호출로 수정** (5분): 단순 텍스트 변경
2. **`update-config.md` 신규 작성** (30분): 기존 스킬 패턴 참고해 작성
3. **훅 경로 절대 경로로 변경** (5분): `settings.json` 한 줄 수정
4. **로그 파싱 공통 라이브러리 추출** (1시간): `.claude/lib/skill_stat_parser.py` 작성
