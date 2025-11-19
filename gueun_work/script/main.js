// --- 기존 경로 검색 기능 ---
document.getElementById("searchBtn")?.addEventListener("click", () => {
  const inputs = getSearchInputs();
  if (!inputs) return;

  const routes = calculateRoute(inputs.start, inputs.end);

  const resultBox = document.getElementById("resultText");
  resultBox.innerHTML = "<h3>추천 경로</h3>";
  routes.forEach(route => {
    resultBox.innerHTML += `
      <div style="margin-bottom: 15px;">
        <strong>${route.type}</strong><br>
        ${route.path}<br>
        거리: ${route.distance} / 시간: ${route.time}
      </div>
      <hr>
    `;
  });
});

// --- 로그인 모달 관련 기능 ---
const loginBtn = document.querySelector(".login-btn");
const modal = document.getElementById("loginModal");
const submitBtn = document.getElementById("submitLogin");

// 로그인 버튼 클릭 → 모달 열기
loginBtn?.addEventListener("click", () => {
  modal.style.display = "flex";
});

// 모달 배경 클릭 → 닫기
modal?.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// 모달 안 로그인 처리
submitBtn?.addEventListener("click", () => {
  const id = document.getElementById("userId").value;
  const pw = document.getElementById("userPw").value;

  if (id === "user" && pw === "1234") {
    alert("로그인 성공!");
    modal.style.display = "none";
  } else {
    alert("아이디 또는 비밀번호가 틀렸습니다.");
  }
});
