// 출발지, 도착지 입력값 받기
function getSearchInputs() {
  const start = document.getElementById("start").value.trim();
  const end = document.getElementById("end").value.trim();

  if (!start || !end) {
    alert("출발지와 도착지를 모두 입력해주세요!");
    return null;
  }

  return { start, end };
}
