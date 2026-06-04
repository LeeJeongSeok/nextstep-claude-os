개발 관련 유튜브 영상에서 주요 인사이트와 학습 개념을 추출하세요.

## 입력 URL

$ARGUMENTS

## 절차

### 1. URL 검증

`$ARGUMENTS`가 비어 있으면 아래를 출력하고 종료하세요.

```
사용법: /yt-learn <YouTube URL>
예시:   /yt-learn https://www.youtube.com/watch?v=dQw4w9WgXcQ

지원 형식:
  https://www.youtube.com/watch?v=VIDEO_ID
  https://youtu.be/VIDEO_ID
  https://www.youtube.com/shorts/VIDEO_ID
```

URL이 YouTube 도메인(`youtube.com` 또는 `youtu.be`)이 아니면 "YouTube URL만 지원합니다."라고 안내하고 종료하세요.

### 2. 비디오 ID 추출 및 영상 정보 수집

아래 스크립트로 비디오 ID를 추출하세요.

```bash
python3 << 'PYEOF'
import re, sys

url = "$ARGUMENTS".strip()

patterns = [
    r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    r'youtu\.be/([a-zA-Z0-9_-]{11})',
    r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
    r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
]

video_id = None
for p in patterns:
    m = re.search(p, url)
    if m:
        video_id = m.group(1)
        break

if video_id:
    print(video_id)
else:
    print("ERROR: 비디오 ID를 추출할 수 없습니다.")
PYEOF
```

스크립트 출력이 `ERROR`로 시작하면 "올바른 YouTube URL을 입력해주세요."라고 안내하고 종료하세요.
추출한 비디오 ID를 `VIDEO_ID`로 기억하세요.

### 3. 영상 기본 정보 수집

WebFetch로 아래 URL에서 영상 제목·채널명·설명을 가져오세요.

- `https://www.youtube.com/watch?v=VIDEO_ID`

페이지에서 아래 정보를 추출하세요.
- 제목 (`<title>` 태그 또는 `"title":` JSON 필드)
- 채널명
- 영상 설명 (첫 500자)

### 4. 자막(transcript) 수집

WebFetch로 아래 URL을 순서대로 시도해 자막을 가져오세요.

1. 한국어 자막: `https://www.youtube.com/api/timedtext?v=VIDEO_ID&lang=ko`
2. 영어 자막: `https://www.youtube.com/api/timedtext?v=VIDEO_ID&lang=en`
3. 자동 생성 자막: `https://www.youtube.com/api/timedtext?v=VIDEO_ID&lang=ko&kind=asr`
4. 자동 생성 자막(영어): `https://www.youtube.com/api/timedtext?v=VIDEO_ID&lang=en&kind=asr`

자막을 가져왔다면 XML에서 텍스트만 추출해 분석에 사용하세요.
자막을 가져오지 못했다면 영상 설명과 WebSearch 결과로 분석하세요.

### 5. 개발 영역 확인

수집한 정보(제목·설명·자막)를 바탕으로 영상이 개발 관련 콘텐츠인지 판단하세요.

개발 관련 영역 예시:
- 프로그래밍 언어, 프레임워크, 라이브러리
- 소프트웨어 아키텍처, 디자인 패턴
- DevOps, 인프라, 클라우드
- 알고리즘, 자료구조
- 개발 도구, IDE, 워크플로우
- 시스템 설계, 데이터베이스
- AI/ML 엔지니어링

개발 관련이 아니라고 판단되면:

```
이 영상은 개발 관련 콘텐츠가 아닌 것으로 보입니다.
제목: {영상 제목}

/yt-learn은 개발 영역 영상만 지원합니다.
```

를 출력하고 종료하세요.

### 6. 보충 검색 (자막이 없는 경우)

자막을 가져오지 못한 경우, WebSearch로 영상 내용을 보충하세요.

검색 쿼리 예시:
- `"{영상 제목}" {채널명} 요약`
- `"{영상 제목}" 핵심 내용`

### 7. 결과 출력

아래 형식으로 출력하세요.

---

## 📺 {영상 제목}

> **채널:** {채널명}
> **URL:** $ARGUMENTS
> **분석 기반:** 자막 전문 / 영상 설명 + 검색 (자막 없음)

---

### 개발 영역 분류

{영상이 해당하는 분야를 태그 형식으로 표시}
예: `#백엔드` `#Spring` `#아키텍처` `#DDD`

---

### 주요 인사이트

> 영상에서 말하는 핵심 메시지나 주장

1. **{인사이트 제목}** — {한 줄 설명}
2. **{인사이트 제목}** — {한 줄 설명}
3. **{인사이트 제목}** — {한 줄 설명}
4. **{인사이트 제목}** — {한 줄 설명}
5. **{인사이트 제목}** — {한 줄 설명}

---

### 학습 개념 목록

영상에서 등장하는 기술·개념·도구를 분류해서 나열하세요.

| 분류 | 개념 / 기술 | 난이도 | 한 줄 설명 |
|------|------------|--------|-----------|
| 언어·프레임워크 | {이름} | 입문/중급/고급 | {설명} |
| 패턴·방법론 | {이름} | 입문/중급/고급 | {설명} |
| 도구·인프라 | {이름} | 입문/중급/고급 | {설명} |

---

### 추천 학습 순서

영상 내용을 토대로 이 주제를 처음 접하는 개발자를 위한 학습 순서를 제안하세요.

1. **{선행 개념}** — 이유: {왜 먼저 알아야 하는지}
2. **{핵심 개념}** — 이유: {왜 이 순서인지}
3. **{심화 개념}** — 이유: {왜 마지막인지}

---

### 더 깊이 공부하려면

WebSearch로 확인한 관련 공식 문서나 자료만 나열하세요.

- [{자료명}]({URL}) — {한 줄 설명}

---

## 출력 규칙

- 자막이 있으면 실제 발화 내용에 근거해 인사이트를 추출하세요. 임의로 만들지 마세요.
- 자막이 없으면 추측임을 명시하세요: "(영상 설명 기반 추정)"
- 개념 설명은 해당 기술을 처음 듣는 개발자 기준으로 쉽게 작성하세요.
- 영상에 등장하지 않은 개념은 목록에 포함하지 마세요.
- 더 깊이 공부하려면 섹션의 URL은 WebSearch로 확인한 것만 사용하세요.
