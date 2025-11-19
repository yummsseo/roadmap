var map = new Tmapv2.Map("map", {
    center: new Tmapv2.LatLng(37.5665, 126.9780), // 서울시청
    zoom: 15
});

var marker;


document.getElementById("searchLocation").addEventListener("click", function () {
    const keyword = document.getElementById("location").value.trim();
    if (!keyword) {
        alert("장소를 입력해주세요!");
        return;
    }
    searchPOI(keyword);
});


function searchPOI(keyword) {
    const url =
        `https://apis.openapi.sk.com/tmap/pois?version=1&format=json&callback=result` +
        `&appKey=HRfwcjIwBt78mOxVBBGYH6MSQKPcv7SzadLC0GXh` +
        `&searchKeyword=${encodeURIComponent(keyword)}&resCoordType=WGS84GEO&reqCoordType=WGS84GEO`;

    fetch(url)
        .then(response => response.json())
        .then(data => {

            if (!data.searchPoiInfo || data.searchPoiInfo.totalCount == "0") {
                alert("검색 결과가 없습니다. 정확한 장소를 입력해주세요!");
                return;
            }

            
            const poi = data.searchPoiInfo.pois.poi[0];

            const lat = parseFloat(poi.frontLat);
            const lon = parseFloat(poi.frontLon);

        
            if (marker) marker.setMap(null);

            
            marker = new Tmapv2.Marker({
                position: new Tmapv2.LatLng(lat, lon),
                map: map
            });

            
            map.setCenter(new Tmapv2.LatLng(lat, lon));
            map.setZoom(17);
        })
        .catch(err => {
            console.log(err);
            alert("장소 검색 중 오류가 발생했습니다.");
        });
}
document.getElementById("submitSuggest").addEventListener("click", function(e) {
    e.preventDefault(); 

    showConfirmPopup();
});


function showConfirmPopup() {
    const popup = document.createElement("div");
    popup.classList.add("popup-overlay");

    popup.innerHTML = `
        <div class="popup-box">
            <h3>건의내용 제출</h3>
            <p>입력하신 내용으로  제출하시겠습니까?</p>
            <div class="popup-buttons">
                <button id="confirmYes">확인</button>
                <button id="confirmNo">취소</button>
            </div>
        </div>
    `;

    document.body.appendChild(popup);

    document.getElementById("confirmYes").onclick = () => {
        document.getElementById("suggestForm").submit(); // 실제 제출
    };

    document.getElementById("confirmNo").onclick = () => {
        popup.remove();
    };
}


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

