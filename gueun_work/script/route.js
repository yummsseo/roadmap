// 경로 계산 (임시 데이터)
function calculateRoute(start, end) {
  const routes = [
    {
      type: "기본 경로",
      path: `${start} → ${end}`,
      distance: "2.4km",
      time: "약 18분"
    },
    {
      type: "장애물 회피 경로",
      path: `${start} → 공원길 → ${end}`,
      distance: "2.6km",
      time: "약 20분"
    },
    {
      type: "편의시설 우선 경로",
      path: `${start} → 엘리베이터 → ${end}`,
      distance: "2.8km",
      time: "약 22분"
    }
  ];
  return routes;
}
