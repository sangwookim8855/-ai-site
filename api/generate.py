from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

MAX_LEN = 100

SYSTEM = "당신은 대학생에게 도로공학을 쉽게 가르치는 조교입니다. 한국어로, 정확하고 간결하게 답하세요. 확실하지 않은 수치는 단정하지 말고 교재 확인을 권하세요."

PROMPTS = {
    "explain": "다음 도로공학 개념을 대학생 눈높이로 설명해 주세요. 정의, 핵심 포인트 3가지, 쉬운 예시 1개 순서로 써 주세요.\n개념: {topic}",
    "quiz": "다음 주제로 객관식 문제 3개를 만들어 주세요. 각 문제는 보기 4개(①~④)를 주고, 마지막에 정답과 짧은 해설을 한꺼번에 적어 주세요.\n주제: {topic}",
}


def ask_ai(mode, topic):
    key = os.environ.get("OPENAI_API_KEY")
    base = os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("OPENAI_MODEL")
    if not key or not base or not model:
        raise RuntimeError("NO_CONFIG")
    url = base.rstrip("/") + "/chat/completions"
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPTS[mode].format(topic=topic)},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self._send(400, {"error": "잘못된 요청입니다."})

        mode = data.get("mode")
        topic = str(data.get("topic", "")).strip()

        if mode not in PROMPTS:
            return self._send(400, {"error": "지원하지 않는 기능입니다."})
        if not topic:
            return self._send(400, {"error": "주제를 입력해 주세요."})
        if len(topic) > MAX_LEN:
            return self._send(400, {"error": "입력은 100자 이내로 해 주세요."})

        try:
            result = ask_ai(mode, topic)
            return self._send(200, {"result": result})
        except RuntimeError:
            return self._send(500, {"error": "서버 설정 오류입니다. (환경 변수 없음)"})
        except urllib.error.HTTPError as e:
            return self._send(502, {"error": "AI 서비스 오류가 발생했습니다. (코드 " + str(e.code) + ")"})
        except (urllib.error.URLError, TimeoutError):
            return self._send(504, {"error": "AI 응답이 지연되고 있습니다. 잠시 후 다시 시도해 주세요."})
        except (KeyError, IndexError):
            return self._send(502, {"error": "AI가 답변을 만들지 못했습니다. 다른 표현으로 시도해 주세요."})
        except Exception:
            return self._send(500, {"error": "알 수 없는 오류가 발생했습니다."})
