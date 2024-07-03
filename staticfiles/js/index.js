
// btns.forEach(function (item, index) {
//   item.addEventListener("click", function () {
//     btns.forEach(function (item, index) {
//       item.classList.remove("active_button");
//     });
//     item.classList.add("active_button");
//   });
// });

document.querySelectorAll("#btns").forEach((item) => {
  item.addEventListener("click", () => {
    document
      .querySelectorAll("#btns")
      .forEach((btn) => btn.classList.remove("active_button"));
    item.classList.add("active_button");
  });
});
