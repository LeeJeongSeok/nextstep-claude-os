현재 브랜치를 원격 저장소에 push하세요.

## 절차

1. `git status`로 커밋되지 않은 변경사항이 있는지 확인하세요.
   - 미커밋 변경사항이 있으면 "먼저 `/git-commit`으로 커밋하세요."라고 안내하고 종료하세요.

2. `git log origin/<브랜치>..HEAD` 로 push할 커밋 목록을 확인하세요.
   - push할 커밋이 없으면 "원격과 동기화되어 있습니다. push할 내용이 없습니다."라고 안내하고 종료하세요.

3. push할 커밋 목록을 출력하세요.

4. `$ARGUMENTS`가 `--force` 또는 `-f`이면:
   - main/master 브랜치에 force push 시도 시 "main/master에는 force push할 수 없습니다."라고 경고하고 종료하세요.
   - 다른 브랜치라면 `git push --force-with-lease`를 실행하세요.

5. 일반 push: `git push` 를 실행하세요.
   - 업스트림이 없으면 `git push -u origin <현재 브랜치명>`으로 실행하세요.

6. push 완료 후 아래 정보를 출력하세요.
   - push한 브랜치명
   - push한 커밋 수
   - 원격 저장소 URL

## 주의사항

- force push는 `--force-with-lease`만 허용합니다 (`--force` 플래그는 사용하지 마세요).
- push 실패 시 오류 메시지를 그대로 출력하고 원인을 한 줄로 설명하세요.
