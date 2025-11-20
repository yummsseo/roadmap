function loginUser() {
    const id = document.getElementById("id").value;
    const email = document.getElementById("email").value;

    
    localStorage.setItem("userName", id);
    localStorage.setItem("userEmail", email);

    alert("로그인 성공!");
    location.href = "setting.html";
}
