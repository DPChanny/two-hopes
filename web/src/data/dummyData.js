export const groups = [
  {
    id: 1,
    title: "텃밭 나눔 모임",
    location: "수원시 영통구 영통1동",
    crops: [
      { id: 101, name: "토마토", status: "미수확" },
      { id: 102, name: "상추", status: "수확 완료" },
    ],
  },
  {
    id: 2,
    title: "주말 작물 교류회",
    location: "수원시 권선구 서둔동",
    crops: [
      { id: 103, name: "고추", status: "수확 완료" },
      { id: 104, name: "가지", status: "미수확" },
    ],
  },
  {
    id: 3,
    title: "토마토 키우기 워크숍",
    location: "수원시 장안구 정자동",
    crops: [
      { id: 105, name: "방울토마토", status: "미수확" },
      { id: 106, name: "청경채", status: "수확 완료" },
      { id: 107, name: "오이", status: "미수확" },
    ],
  },
  {
    id: 4,
    title: "도시농업 새싹모임",
    location: "용인시 기흥구 상하동",
    crops: [
      { id: 108, name: "열무", status: "수확 완료" },
      { id: 109, name: "상추", status: "미수확" },
    ],
  },
  {
    id: 5,
    title: "친환경 농법 공유회",
    location: "성남시 수정구 복정동",
    crops: [
      { id: 110, name: "케일", status: "미수확" },
      { id: 111, name: "비트", status: "미수확" },
      { id: 112, name: "토마토", status: "수확 완료" },
    ],
  },
  {
    id: 6,
    title: "작물 초보 모임",
    location: "수원시 팔달구 매산동",
    crops: [
      { id: 113, name: "상추", status: "미수확" },
      { id: 114, name: "당근", status: "미수확" },
    ],
  },
];

export const cropPosts = [
  {
    id: 1,
    cropId: 101,
    postImg: "../assets/tomato.png",
    content: "요즘 비가 자주 와서 물 주는 주기를 줄였어요.",
    liked: false,
  },
  {
    id: 2,
    cropId: 101,
    content: "토마토가 벌써 익었어요! 수확했어요 🍅",
    liked: true,
  },
  {
    id: 3,
    cropId: 102,
    content: "상추가 조금 시들했는데 다시 살아났어요.",
    liked: false,
  },
  {
    id: 4,
    cropId: 103,
    content: "고추에 벌레가 생겨서 방제 중이에요.",
    liked: false,
  },
];
