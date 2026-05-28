현재 진행 중인 작업의 상태를 출력합니다.

## 실행 절차

1. `.claude/context/current.md` 파일을 읽으세요.
2. 파일이 없으면 "진행 중인 작업이 없습니다. `/task <요구사항>`으로 새 작업을 시작하세요."라고 안내하세요.
3. 파일이 있으면 아래 형식으로 현재 상태를 출력하세요.

## 출력 형식

```
📋 현재 작업 상태

🆔 작업 ID: {id}
📌 상태: {status 한국어 변환}
🕐 시작: {created}
🔄 최종 업데이트: {updated}

📝 요구사항
{원본 요구사항}

📊 진행 단계
{각 단계별 완료 여부를 ✅/⏳/⬜로 표시}
  ✅/⏳/⬜ 1단계 해석 (interpret)
  ✅/⏳/⬜ 2단계 구조화 (structure)
  ✅/⏳/⬜ 3단계 구현 (implement)
  ✅/⏳/⬜ 4단계 기록 (record)

🚧 블로커 (있는 경우)
{블로커 내용}

⏭ 다음 행동
{다음 행동 내용}
```

## status 한국어 변환 기준

- `new` → 시작 전
- `interpreting` → 해석 중
- `interpreted` → 해석 완료
- `structuring` → 구조화 중
- `structured` → 구조화 완료
- `implementing` → 구현 중
- `implemented` → 구현 완료
- `recording` → 기록 중
- `done` → 완료
- `blocked` → 블로킹
