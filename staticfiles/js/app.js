// Function to safely add event listeners
const addEventListenerSafely = (selector, event, handler) => {
  const element = document.querySelector(selector);
  if (element) {
    element.addEventListener(event, handler);
  }
};

// Function to toggle classes
const toggleClasses = (element, ...classes) => {
  if (element) {
    classes.forEach((cls) => element.classList.toggle(cls));
  }
};

// Function to add and remove classes
const addClasses = (element, ...classes) => {
  if (element) {
    classes.forEach((cls) => element.classList.add(cls));
  }
};

const removeClasses = (element, ...classes) => {
  if (element) {
    classes.forEach((cls) => element.classList.remove(cls));
  }
};

// Toggle search box
addEventListenerSafely("#header__search__btn", "click", () => {
  const headerSearchBox = document.querySelector("#header__search__box");
  toggleClasses(
    headerSearchBox,
    "max-w-[36px]",
    "md:max-w-[320px]",
    "max-w-[320px]",
    "gap-2"
  );
});

// Close responsive nav
const closeResNav = () => {
  const resNav = document.querySelector("#res__nav");
  const resNavBackdrop = document.querySelector("#res__nav__backdrop");
  const body = document.body;
  addClasses(resNav, "right-[-100%]");
  removeClasses(resNav, "right-0");
  addClasses(resNavBackdrop, "hidden");
  removeClasses(resNavBackdrop, "block");
  removeClasses(body, "h-screen", "overflow-hidden");
};

addEventListenerSafely("#res__nav___close__btn", "click", closeResNav);
addEventListenerSafely("#res__nav__backdrop", "click", closeResNav);

// Open responsive nav
addEventListenerSafely("#hamburger__btn", "click", () => {
  const resNav = document.querySelector("#res__nav");
  const resNavBackdrop = document.querySelector("#res__nav__backdrop");
  const body = document.body;
  removeClasses(resNav, "right-[-100%]");
  addClasses(resNav, "right-0");
  addClasses(resNavBackdrop, "block");
  removeClasses(resNavBackdrop, "hidden");
  addClasses(body, "h-screen", "overflow-hidden");
});

// Highlight problem card
document.querySelectorAll("#problem_b_card").forEach((item, index, array) => {
  item.addEventListener("click", () => {
    array.forEach((card) => removeClasses(card, "bg-[#E7E2E2]"));
    addClasses(item, "bg-[#E7E2E2]");
  });
});

// Toggle big menu
addEventListenerSafely("#header__big__menu__open", "click", () => {
  const headerBigMenu = document.querySelector("#header__big__menu");
  toggleClasses(headerBigMenu, "top-20", "bottom-[-100%]");
  document.body.classList.toggle("overflow-hidden")
});

addEventListenerSafely("#header__big__menu__backdrop", "click", () => {
  const headerBigMenu = document.querySelector("#header__big__menu");
  removeClasses(headerBigMenu, "top-20");
  addClasses(headerBigMenu, "bottom-[-100%]");
  document.body.classList.remove("overflow-hidden")
});

// Toggle responsive big menu
addEventListenerSafely("#res__big__menu", "click", () => {
  const resBigMenu = document.querySelector("#res__big__menu");
  toggleClasses(resBigMenu, "h-[270px]", "h-[20px]");
});

// Toggle profile xizmat text
document.querySelectorAll(".profile__xizmat__text").forEach((item, index) => {
  const profileXizmatClose = document.querySelectorAll(
    ".profile__xizmat__close"
  )[index];
  item.addEventListener("click", () => {
    toggleClasses(item, "bg-[#D8D8D8]", "bg-[#F0F6FA]");
    if (profileXizmatClose) {
      toggleClasses(profileXizmatClose, "hidden");
    }
  });
});

// Validate password reset form
addEventListenerSafely("#res__pas__btn", "click", (e) => {
  e.preventDefault();

  const pas1 = document.querySelector("#pas1");
  const pas2 = document.querySelector("#pas2");
  const validationResNav = document.querySelector("#validation__res__nav");
  const validationResNav1 = document.querySelector("#validation__res__nav_1");

  const toggleVisibility = (element) => {
    if (element) {
      element.classList.toggle("hidden");
      element.classList.toggle("block");
    }
  };

  if (pas1 && pas1.value === "") {
    toggleVisibility(validationResNav1);

    setTimeout(() => {
      toggleVisibility(validationResNav1);
    }, 3000);
  }

  if (pas1 && pas2 && pas1.value === pas2.value) {
    addClasses(validationResNav, "hidden");
    removeClasses(validationResNav, "block");
  } else {
    addClasses(validationResNav, "block");
    removeClasses(validationResNav, "hidden");
  }
});

let problem__btn__1 = document.querySelectorAll(".problem__btn__1");
let problem__btn__2 = document.querySelectorAll(".problem__btn__2");
let problem_nav_1 = document.querySelector(".problem_nav_1");
let problem_nav_2 = document.querySelector(".problem_nav_2");
let probleb__b_box = document.querySelector("#probleb__b_box");
let problem__btn = document.querySelectorAll(".problem__btn");

problem__btn.forEach(function (item, index) {
  item.addEventListener("click", function () {
    problem__btn.forEach(function (item, index) {
      item.classList.remove("problem__btn__1__active");
    });
    probleb__b_box.style.display = "none";
  });
});

problem__btn__1.forEach(function (item, index) {
  item.addEventListener("click", function () {
    problem__btn__1[index].classList.toggle("problem__btn__1__active");
    problem_nav_1.classList.remove("problem__un__active");
    problem_nav_2.classList.add("problem__un__active");
  });
});
problem__btn__2.forEach(function (item, index) {
  item.addEventListener("click", function () {
    problem__btn__2[index].classList.toggle("problem__btn__1__active");
    problem_nav_2.classList.remove("problem__un__active");
    problem_nav_1.classList.add("problem__un__active");
  });
});
let profile__modal__open = document.querySelectorAll(".profile__modal__open");
let profile__modal__close = document.querySelector(".profile__modal__close");
let profil__galereya__modal = document.querySelector(
  ".profil__galereya__modal"
);
let profil__galereya__modal__img = document.querySelector(".profil__galereya__modal__img")

profile__modal__open.forEach(function (item, index) {
  item.addEventListener("click", function () {
    profil__galereya__modal.classList.remove("scale-0");
    profil__galereya__modal.classList.add("scale-100");
    profile__modal__close.classList.add("block")
    profile__modal__close.classList.remove("hidden")
  });
});
profile__modal__close.addEventListener("click", function () {
    profil__galereya__modal.classList.remove("scale-100");
    profil__galereya__modal.classList.add("scale-0");
  profile__modal__close.classList.add("hidden")
  profile__modal__close.classList.remove("block")
});