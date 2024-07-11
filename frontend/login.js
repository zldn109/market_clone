const form = document.querySelector("#login-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const sha256Password = sha256(formData.get("password"));
  //   폼데이터의 password내에 있는 데이터를 받아와서 sha256으로 변환
  formData.set("password", sha256Password);
  //   formData 내에서 우리가 signup.html에서 password라고 name 지었던 것에 sha256Password를 설정하기

  //   const div = document.querySelector("#info");
  const res = await fetch("/login", {
    method: "post",
    body: formData,
  });
  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다!");
  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmitForm);
