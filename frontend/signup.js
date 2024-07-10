const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmitForm = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  //   폼데이터의 password내에 있는 데이터를 받아와서 sha256으로 변환
  formData.set("password", sha256Password);
  //   formData 내에서 우리가 signup.html에서 password라고 name 지었던 것에 sha256Password를 설정하기

  const div = document.querySelector("#info");
  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "post",
      body: formData,
    });
    const data = await res.json();
    if (data === "200") {
      div.innerText = "회원가입에 성공했습니다!";
      div.style.color = "blue";
      alert("회원가입에 성공했습니다.");
      window.location.pathname = "/login.html";
    }
  } else {
    div.innerText = "비밀번호가 일치하지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmitForm);
