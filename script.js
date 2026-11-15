const menuBtn = document.getElementById("menuBtn");
const nav = document.getElementById("nav");
menuBtn.addEventListener("click", () => nav.classList.toggle("open"));
nav.addEventListener("click", () => nav.classList.remove("open"));

async function callAI(mode, inputId, button, box) {
  const topic = document.getElementById(inputId).value.trim();
  if (!topic) {
    box.textContent = "주제를 입력해 주세요.";
    return;
  }
  button.disabled = true;
  box.textContent = "AI가 답변을 만드는 중입니다...";
  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: mode, topic: topic })
    });
    const data = await res.json();
    box.textContent = res.ok ? data.result : (data.error || "오류가 발생했습니다.");
  } catch (e) {
    box.textContent = "서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.";
  } finally {
    button.disabled = false;
  }
}

const explainBtn = document.getElementById("explainBtn");
const quizBtn = document.getElementById("quizBtn");
explainBtn.addEventListener("click", () =>
  callAI("explain", "topicExplain", explainBtn, document.getElementById("explainResult")));
quizBtn.addEventListener("click", () =>
  callAI("quiz", "topicQuiz", quizBtn, document.getElementById("quizResult")));