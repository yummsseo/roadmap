document.getElementById("searchBtn").addEventListener("click", function () {
  const start = document.getElementById("start").value.trim();
  const end = document.getElementById("end").value.trim();

  if (start === "" || end === "") {
    alert("출발지와 도착지를 모두 입력해주세요.");
    return;
  }

  console.log(`출발지: ${start}, 도착지: ${end}`);
  document.getElementById("resultText").textContent = `출발지: ${start} → 도착지: ${end}`;
});
