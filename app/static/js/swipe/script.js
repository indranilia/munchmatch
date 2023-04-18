import { post, get } from "../_api.js";
import { getFormData, initPlacesAPI } from "../_helper.js";
import { getImageFromGoogleImages } from "../integrations/google.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

// DOM
const swipper = document.getElementById("swipper");
const swipe_forward = document.getElementById("swipe_forward");
const swipe_backward = document.getElementById("swipe_backward");
const newDishButton = document.getElementById("new_dish");
const newDishModalContainer = document.getElementById("add_new_dish_modal");
const newDishModal = newDishModalContainer.getElementsByClassName("modal")[0];
const newDishForm = document.getElementById("new_dish_form");

initPlacesAPI("location_input_new_meal", (newValue) => {
  currentPreferences.location = newValue.formatted_address;
  saveOtherPreferences();
});

let meals = [];
let tempMeals = [];

const getInitialDishes = async () => {
  const response = await get(`/swipe/meals`);
  meals = response.data.data;
  const tempMeals = [];
  for (const dish of response.data.data) {
    tempMeals.push(await createDish(dish, false));
  }

  for (const meal of tempMeals) {
    swipper.append(meal);
  }
};

async function createDish(newDish, append = true) {
  const picture = await getImageFromGoogleImages(
    newDish.name,
    undefined,
    false
  );
  const dish = new Dish({
    picture: newDish.picture || picture,
    price: newDish.price,
    name: newDish.name,
    location: newDish.location || "",
    rate: newDish.rate,

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

  if (append) {
    swipper.prepend(dish.element);
  } else {
    return dish.element;
  }
}

function updateDishes() {
  const dishes = swipper.querySelectorAll(".dish:not(.dismissing)");
  dishes.forEach((dish, index) => {
    dish.style.setProperty("--i", index);
  });
}

const getNextMeal = async (swippedMealUUID, direction) => {
  const response = await post(
    `/swipe/swipe/${swippedMealUUID}/${direction}`,
    {},
    undefined,
    undefined,
    false
  );
  const status = response.status;
  const newMeals = response.data.data;
  const exitingMeals = [...meals].map((card) => card.uuid);
  const newMeal = newMeals.filter(
    (meal) => !exitingMeals.includes(meal.uuid) && meal.uuid !== swippedMealUUID
  )[0];

  if (newMeal) {
    meals.push(newMeal);
    createDish(newMeal);
  }
};

getInitialDishes();

updateDishes();

newDishButton.addEventListener("click", () => {
  newDishModalContainer.classList.add("visible");
});

newDishModalContainer.addEventListener("click", () => {
  newDishModalContainer.classList.remove("visible");
});

newDishModal.addEventListener("click", (event) => {
  event.stopPropagation();
});

newDishForm.addEventListener("submit", async (event) => {
  try {
    event.preventDefault();
    const obj = getFormData(event, newDishForm);
    const newSrc = await getImageFromGoogleImages(obj["name"]);
    obj.picture = newSrc;
    const { data, status } = await post("/meal", obj);

    if (status === 201) {
      newDishModalContainer.classList.remove("visible");
      successToast("Meal added successfully!");
      createDish(data.newMeal);
      updateDishes();

      return;
    }

    errorToast("An error has occurred. Try again");
  } catch (error) {
    errorToast(error.message);
  }
});
