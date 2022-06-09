/*=============== FULLWIDTH GRID || 3 COLUMN GRID SWITCH LAYOUT ===============*/

let listFull = document.querySelector(".list-full");
let listHalf = document.querySelector(".list-half");
let listContainer = document.querySelector(".listing__container");

listHalf.addEventListener("click", () => {
  listContainer.classList.add("active");
  listHalf.classList.add("active");
  listFull.classList.remove("active");
});

listFull.addEventListener("click", () => {
  listContainer.classList.remove("active");
  listHalf.classList.remove("active");
  listFull.classList.add("active");
});
