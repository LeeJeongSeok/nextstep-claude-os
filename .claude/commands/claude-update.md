Claude Code 최신 업데이트를 확인하고 설치하세요.

## 절차

### 1. 버전 비교

아래 명령을 실행해 현재 버전과 최신 버전을 확인하세요.

```bash
CURRENT=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
LATEST=$(npm view @anthropic-ai/claude-code version 2>/dev/null)
echo "현재 버전: $CURRENT"
echo "최신 버전: $LATEST"
if [ "$CURRENT" = "$LATEST" ]; then
  echo "STATUS=up-to-date"
else
  echo "STATUS=update-available"
fi
```

- `STATUS=up-to-date`이면 "이미 최신 버전입니다 (v$CURRENT)." 출력 후 종료
- `STATUS=update-available`이면 다음 단계로 진행

### 2. 릴리즈 노트 확인

WebSearch로 업데이트 내용을 검색하세요.

검색 쿼리:
- `Claude Code $LATEST release notes changelog`
- `@anthropic-ai/claude-code $LATEST 업데이트 새 기능`

검색 결과에서 주요 변경사항을 아래 형식으로 정리하세요.

```
## Claude Code 업데이트: v$CURRENT → v$LATEST

### 주요 변경사항
- 변경 항목 1
- 변경 항목 2
- ...

### 버그 수정
- 수정 항목 1
- ...
```

검색으로 확인되지 않으면 "릴리즈 노트를 찾을 수 없습니다." 로 표시하고 계속 진행하세요.

### 3. 업데이트 실행

아래 명령으로 업데이트하세요.

```bash
npm install -g @anthropic-ai/claude-code@latest
```

- 오류 발생 시 오류 메시지를 그대로 출력하고 원인을 한 줄로 설명하세요.
- 권한 오류(`EACCES`)가 발생하면 "sudo npm install -g @anthropic-ai/claude-code@latest 를 직접 실행하세요." 안내 후 종료하세요.

### 4. 업데이트 검증

```bash
NEW_VERSION=$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "설치된 버전: $NEW_VERSION"
```

### 5. 완료 출력

```
업데이트 완료
  이전 버전: v$CURRENT
  현재 버전: v$NEW_VERSION
```

## 주의사항

- 업데이트 전 실행 중인 Claude Code 세션이 있으면 재시작이 필요할 수 있습니다.
- npm 전역 설치 경로에 쓰기 권한이 없으면 sudo가 필요합니다.
