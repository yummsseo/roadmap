document.getElementById("findRoutes").addEventListener("click", () => {
  const departure = document.getElementById("departure").value.trim();
  const destination = document.getElementById("destination").value.trim();

  if (!departure || !destination) {
    alert("출발지와 도착지를 모두 입력해주세요!");
    return;
  }

  
  alert(`경로를 검색합니다!\n출발: ${departure}\n도착: ${destination}`);

  const mapBox = document.querySelector(".map-box p");
  mapBox.textContent = `현재 ${departure} → ${destination} 경로 탐색 중...`;
});

document.getElementById("submitReport").addEventListener("click",function(event){
  event.preventDefault();

  const result = confirm("제출하시겠습니까?");

  if(result){
    this.ariaLabelledByElements("제출되었습니다. 감사합니다.");
    document.getElementById("reportForm").reset();
  }else{
    alert("취소되었습니다.");
  }
})

document.addEventListener("DOMContentLoaded",()=>{
  const form=document.getElementById("signupForm");

  if(form){
    form.addEventListener("submit",function(e){
      e.preventDefault();

      alert("계정이 생성되었습니다.");

      form.reset();
    })
  }
})