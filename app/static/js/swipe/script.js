import { post, get } from "../_api.js";
import { getImageFromGoogleImages } from "../integrations/google.js";

// DOM
const swiper = document.getElementById("swiper");
const swipe_forward = document.getElementById("swipe_forward");
const swipe_backward = document.getElementById("swipe_backward");

let meals = [];

const getInitialDishes = async () => {
  const response = await get(`/swipe/meals`);
  console.log(response);
  meals = response.data.data;
  for (const dish of response.data.data) {
    createDish(dish);
  }
};

async function createDish(newDish) {
  const picture = await getImageFromGoogleImages(newDish.name);
  const dish = new Dish({
    picture: picture,
    price: newDish.price,
    name: newDish.name,

    onDishLiked: () => {
      swipe_forward.style.animationPlayState = "running";
      swipe_forward.classList.toggle("trigger");
      getNextMeal(newDish.uuid, "right");
    },
    onDishDisliked: () => {
      swipe_backward.style.animationPlayState = "running";
      swipe_backward.classList.toggle("trigger");
      getNextMeal(newDish.uuid, "left");
    },
  });
  swiper.appendChild(dish.element);
}

function updateDishes() {
  const dishes = swiper.querySelectorAll(".dish:not(.dismissing)");
  dishes.forEach((dish, index) => {
    dish.style.setProperty("--i", index);
  });
}

const getNextMeal = async (swippedMealUUID, direction) => {
  const response = await post(
    `/swipe/swipe/${swippedMealUUID}/${direction}`,
    {}
  );
  const status = response.status;
  const newMeals = response.data.data;
  const exitingMeals = [...meals].map((card) => card.uuid);
  const newMeal = newMeals.filter(
    (meal) => !exitingMeals.includes(meal.uuid)
  )[0];

  if (newMeal) {
    createDish(newMeal);
    updateDishes();
  }
};

getInitialDishes();

updateDishes();
