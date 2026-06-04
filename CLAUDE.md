# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`nextstep-claude-os` — 나만의 Claude Code OS. 불명확한 요구·자료·아이디어를 실행 가능한 구조와 산출물로 변환하는 개인 워크플로우 시스템.

## 사용자 컨텍스트 파일

에이전트와 스킬은 아래 파일을 필요에 따라 읽어 산출물을 조율한다.

| 파일 | 내용 | 참조 시점 |
|------|------|-----------|
| `.claude/context/profile.md` | 개발자 레벨, 협업 스타일, 주요 작업 영역 | 요구사항 해석 전 |
| `.claude/context/craft.md` | 코드·문서 품질 기준, 의사결정 원칙 | 구현 시작 전 |

## 핵심 행동 원칙

항상 적용. 별도 지시 없이도 이 원칙을 따른다.

1. **직접 실행 위주** — 결과물 먼저, 설명은 Why가 자명하지 않을 때만 추가
2. **최소 구현** — 지금 당장 필요한 것만. 미래 요구사항은 고려하지 않음
3. **선택지보다 최선안** — 여러 옵션 나열보다 최선 하나를 바로 실행
4. **주니어 시각 보완** — 설계 판단이 필요한 지점에서 이유 한 줄 추가
