# 도로공학 AI 학습 도우미

도로공학 개념을 입력하면 AI가 쉽게 설명해 주고, 이해도를 확인할 객관식 퀴즈를 만들어 주는 웹 서비스입니다.

- 배포 URL: https://road-ai-helper.vercel.app

## 서비스 소개

- **개념 설명**: 궁금한 도로공학 개념(예: 소단, 편절편성토, 펌핑 현상)을 입력하면 정의, 핵심 포인트, 예시를 설명해 줍니다.
- **퀴즈**: 주제를 입력하면 객관식 문제 3개와 정답, 해설을 만들어 줍니다.
- **이용 안내**: 사용 방법과 유의사항을 안내합니다.
- 모바일에서도 보기 편한 반응형 화면입니다.

## 기술 스택

- 프론트엔드: HTML, CSS, JavaScript
- 백엔드: Python (Vercel Serverless Function, `api/generate.py`)
- AI: OpenAI 호환 API (코디세이 API 콘솔, 모델 `gpt-5-mini`)
- 배포: GitHub + Vercel

## 폴더 구조

```
.
├── index.html        # 화면 구성 (메뉴와 섹션)
├── style.css         # 디자인과 반응형 스타일
├── script.js         # 버튼 동작, AI 요청과 결과 표시
├── api/
│   └── generate.py   # AI API를 호출하는 백엔드
├── .gitignore
└── README.md
```

## 환경 변수 설정

API 키는 코드에 직접 적지 않고 환경 변수로 관리합니다. 아래 3개를 설정해야 AI 기능이 동작합니다.

| 이름 | 설명 | 예시 |
|---|---|---|
| `OPENAI_API_KEY` | 발급받은 API 키 | (비공개) |
| `OPENAI_BASE_URL` | AI API 주소 | `https://copa.codyssey.kr/v1` |
| `OPENAI_MODEL` | 사용할 모델 이름 | `gpt-5-mini` |

API 키는 GitHub에 올리지 않습니다. 로컬 테스트용 `.env` 파일은 `.gitignore`에 포함되어 있습니다.

## 배포 방법 (Vercel)

1. 이 저장소를 GitHub에 올립니다.
2. Vercel에서 **Add New → Project**를 눌러 이 저장소를 Import 합니다.
3. **Environment Variables**에 위 3개 환경 변수를 입력합니다.
4. **Deploy**를 누르면 배포가 완료됩니다.
5. 이후 GitHub의 `main` 브랜치에 변경 사항을 올리면 자동으로 다시 배포됩니다.

## 실행 방법 (로컬)

1. Node.js를 설치하고 Vercel CLI를 설치합니다: `npm i -g vercel`
2. 프로젝트 폴더에 환경 변수 3개를 설정합니다.
3. `vercel dev`를 실행하고 안내된 주소로 접속합니다.

## AI 기능 동작

- 입력: 100자 이내의 주제 또는 개념
- 출력: AI가 생성한 설명 또는 퀴즈 텍스트
- 실패 처리: 입력이 비었거나 100자를 넘으면 안내 문구를 보여 주고, AI 서비스 오류나 응답 지연 시 오류 메시지를 화면에 표시합니다.
