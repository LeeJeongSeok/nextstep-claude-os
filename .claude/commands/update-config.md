Claude Code 설정을 조회하거나 변경합니다.

## 입력

$ARGUMENTS

## 실행 절차

### 입력이 없는 경우 — 현재 설정 조회

1. `$ARGUMENTS`가 비어 있으면 아래 파일들을 읽고 현재 설정 상태를 출력하세요:
   - `/Users/jeongseok/Desktop/nextstep/nextstep-claude-os/.claude/settings.json`
   - `/Users/jeongseok/Desktop/nextstep/nextstep-claude-os/.claude/settings.local.json` (있는 경우)

2. 아래 형식으로 출력하세요:

```
현재 Claude Code 설정

[settings.json]
{내용 요약}

[settings.local.json]
{내용 요약 또는 "파일 없음"}

변경하려면: /update-config <변경할 설정 내용>
예시: /update-config 훅 경로를 절대 경로로 변경
      /update-config allowedTools에 Bash(git *) 추가
```

### 입력이 있는 경우 — 설정 변경

1. 요청 내용을 파악해 어떤 파일의 어떤 항목을 변경해야 하는지 결정하세요.
   - 보안에 영향 없는 변경 (경로, 도구 허용 등): `settings.json` 수정
   - 민감한 정보나 로컬 전용 설정: `settings.local.json` 수정

2. 변경 전 현재 값을 출력하고, 변경 내용을 적용하세요.

3. 변경 완료 후 아래 형식으로 보고하세요:

```
설정 변경 완료

변경 파일: {파일명}
변경 내용: {무엇이 어떻게 바뀌었는지 한 줄}
```

## 변경 가능한 설정 예시

| 항목 | 설명 |
|------|------|
| `hooks` | UserPromptSubmit, Stop 등 훅 커맨드 경로·내용 |
| `allowedTools` | 자동 허용할 도구 패턴 (Bash, Read, Write 등) |
| `permissions` | 파일 접근 권한 설정 |
