{
  /* <div class="item-list">
  <div class="item-list__img">
    <img src="assets/image.svg" alt="img" />
  </div>
  <div class="item-list__info">
    <div class="item-list__info-title">블루투스 키보드 팝니다</div>
    <div class="item-list__info-meta">서초동 4시간 전</div>
    <div class="item-list__info-price">5,000원</div>
  </div>
</div>; */
}

const calcTime = (timestamp) => {
  // 한국시간 = UTC + 9시간
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const minute = time.getMinutes();
  const seconds = time.getSeconds();

  if (hour > 0) return `${hour}시간 전`;
  else if (minute > 0) return `${minute}분 전`;
  else if (seconds > 0) return `${second}초 전`;
  else return "방금 전";
};

const renderData = (data) => {
  // data = [{id:1,title:'aa'...},{id:2,title:'bbb'...}..]이런형태
  const main = document.querySelector("main");

  data.reverse().forEach(async (obj) => {
    // 배열 각각에 대해서 반복문 돌리기
    // 리버스해주는 이유는 최근 작성한 것이 위에 올라오도록 하기 위해서 해줌

    const itemListDiv = document.createElement("div");
    itemListDiv.className = "item-list";

    const itemListImgDiv = document.createElement("div");
    itemListImgDiv.className = "item-list__img";

    const img = document.createElement("img");
    const res = await fetch(`/images/${obj.id}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    img.src = url;

    const itemListInfoDiv = document.createElement("div");
    itemListInfoDiv.className = "item-list__info";

    const itemListInfoTitleDiv = document.createElement("div");
    itemListInfoTitleDiv.className = "item-list__info-title";
    itemListInfoTitleDiv.innerText = obj.title;

    const itemListInfoMetaDiv = document.createElement("div");
    itemListInfoMetaDiv.className = "item-list__info-meta";
    itemListInfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const itemListInfoPriceDiv = document.createElement("div");
    itemListInfoPriceDiv.className = "item-list__info-price";
    itemListInfoPriceDiv.innerText = obj.price;

    itemListImgDiv.appendChild(img);

    itemListInfoDiv.appendChild(itemListInfoTitleDiv);
    itemListInfoDiv.appendChild(itemListInfoMetaDiv);
    itemListInfoDiv.appendChild(itemListInfoPriceDiv);

    itemListDiv.appendChild(itemListImgDiv);
    itemListDiv.appendChild(itemListInfoDiv);

    main.appendChild(itemListDiv);
  });
};

const fetchList = async () => {
  const accessToken = window.localStorage.getItem("token");
  const res = await fetch("/items", {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (res.status === 401) {
    alert("로그인이 필요합니다!");
    window.location.pathname = "/login.html";
    return;
  }

  const data = await res.json();
  renderData(data);
};

fetchList();
