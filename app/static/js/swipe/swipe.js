// "use strict";
import { post } from "../_api.js";

const allMealsContainer = document.querySelector(".all-meals-container");
const allMealsCards = document.querySelector(".all-meal-cards");
let allCards = document.querySelectorAll(".meal-card");
const nope = document.getElementById("nope");
const love = document.getElementById("love");

const getNextMeal = async (swippedMealUUID) => {
  const response = await post(`/swipe/swipe/${swippedMealUUID}/right`, {});
  const status = response.status;
  const meals = response.data.data;
  console.log(typeof meals);
  const exitingMeals = [...allCards].map((card) => card.id);
  const newMeal = meals.filter((meal) => !exitingMeals.includes(meal.uuid))[0];

  if (newMeal) addMeal(newMeal);
};

const addMeal = (newMeal) => {
  const lastMeal = allCards[allCards.length - 1].cloneNode(true);
  lastMeal.id = newMeal.uuid;
  console.log(lastMeal);
  const mealImage = lastMeal.querySelectorAll("img")[0];
  mealImage.src = `${window.location.origin}/static/img/pasta.jpeg`;
  mealImage.alt = newMeal.name;

  const mealH2 = lastMeal.querySelectorAll("h2")[0];
  mealH2.innerHTML = newMeal.name;

  const mealP = lastMeal.querySelectorAll("p")[0];
  mealP.innerHTML = newMeal.price;

  lastMeal.style.zIndex = 1;
  lastMeal.style.transform =
    "scale(" + (20 - 2) / 20 + ") translateY(-" + 30 * 2 + "px)";
  lastMeal.style.opacity = (10 - 2) / 10;

  allCards[0].remove();
  allMealsCards.appendChild(lastMeal);
  allCards = document.querySelectorAll(".meal-card");
  createHammer(lastMeal);
};

const initCards = (card, index) => {
  const newCards = document.querySelectorAll(".meal-card:not(.removed)");

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform =
      "scale(" + (20 - index) / 20 + ") translateY(-" + 30 * index + "px)";
    card.style.opacity = (10 - index) / 10;
  });

  allMealsContainer.classList.add("loaded");
};

initCards();

const createHammer = (el) => {
  const hammertime = new Hammer(el);

  hammertime.on("pan", function (event) {
    el.classList.add("moving");
  });

  hammertime.on("pan", function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    allMealsContainer.classList.toggle(
      "all-meals-container_love",
      event.deltaX > 0
    );
    allMealsContainer.classList.toggle(
      "all-meals-container_nope",
      event.deltaX < 0
    );

    const xMulti = event.deltaX * 0.03;
    const yMulti = event.deltaY / 80;
    const rotate = xMulti * yMulti;

    event.target.style.transform =
      "translate(" +
      event.deltaX +
      "px, " +
      event.deltaY +
      "px) rotate(" +
      rotate +
      "deg)";
  });

  hammertime.on("panend", function (event) {
    el.classList.remove("moving");
    allMealsContainer.classList.remove("all-meals-container_love");
    allMealsContainer.classList.remove("all-meals-container_nope");

    const moveOutWidth = document.body.clientWidth;
    const keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle("removed", !keep);

    if (keep) {
      event.target.style.transform = "";
    } else {
      console.log(event.target.getAttribute("id"));
      getNextMeal(event.target.getAttribute("id"));
      const endX = Math.max(
        Math.abs(event.velocityX) * moveOutWidth,
        moveOutWidth
      );
      const toX = event.deltaX > 0 ? endX : -endX;
      const endY = Math.abs(event.velocityY) * moveOutWidth;
      const toY = event.deltaY > 0 ? endY : -endY;
      const xMulti = event.deltaX * 0.03;
      const yMulti = event.deltaY / 80;
      const rotate = xMulti * yMulti;

      event.target.style.transform =
        "translate(" +
        toX +
        "px, " +
        (toY + event.deltaY) +
        "px) rotate(" +
        rotate +
        "deg)";
      initCards();
    }
  });
};

allCards.forEach(function (el) {
  createHammer(el);
});

const createButtonListener = (love) => {
  return function (event) {
    const cards = document.querySelectorAll(".meal-card:not(.removed)");
    const moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    const card = cards[0];

    card.classList.add("removed");

    if (love) {
      card.style.transform =
        "translate(" + moveOutWidth + "px, -100px) rotate(-30deg)";
    } else {
      card.style.transform =
        "translate(-" + moveOutWidth + "px, -100px) rotate(30deg)";
    }

    initCards();

    event.preventDefault();
  };
};

const nopeListener = createButtonListener(false);
const loveListener = createButtonListener(true);

nope.addEventListener("click", nopeListener);
love.addEventListener("click", loveListener);
