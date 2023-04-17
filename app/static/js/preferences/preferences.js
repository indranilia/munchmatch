import { getImageFromGoogleImages } from "../integrations/google.js";
import { get, post } from "../_api.js";
import { initPlacesAPI } from "../_helper.js";

const locationInput = document.querySelector("#location_input_preferences");
initPlacesAPI("location_input_preferences", (newValue) => {
  currentPreferences.location = newValue.formatted_address;
  saveOtherPreferences();
});

const rangeInput = document.querySelector("#range_input_preferences");
rangeInput.addEventListener("change", (event) => {
  currentPreferences.range = event.target.value;
  saveOtherPreferences();
});

let typesSelected = [];
let currentPreferences = {};

const saveOtherPreferences = async () => {
  await post(
    "/preferences/update_preferences",
    { range: currentPreferences.range, location: currentPreferences.location },
    undefined,
    undefined,
    false
  );
};

const getCurrentPreferences = async (pills) => {
  const { data, status } = await get("/preferences/get_preferences");
  currentPreferences = data.preferences;
  typesSelected = currentPreferences.cuisine.map(
    (preference) => preference.name
  );

  for (const pill of pills) {
    const pillText = pill.querySelector("span").innerHTML;
    if (typesSelected.includes(pillText)) {
      pill.classList.add("selected");
    }
  }

  locationInput.value = currentPreferences.location;
  rangeInput.value = currentPreferences.range;
};

const addImagesToPills = async () => {
  const pills = document.getElementsByClassName("cousine-pill");
  getCurrentPreferences(pills);

  for (const pill of pills) {
    const pillImg = pill.querySelector("img");
    const pillText = pill.querySelector("span").innerHTML;
    const googleImg = await getImageFromGoogleImages(
      `${pillText} cuisine cute png icon filetype:png`,
      undefined,
      false
    );
    pillImg.src = googleImg;

    pill.addEventListener("click", async () => {
      if (typesSelected.includes(pillText)) {
        typesSelected = typesSelected.filter((type) => type !== pillText);
        pill.classList.remove("selected");
        currentPreferences.cuisine = currentPreferences.cuisine.filter(
          (cuisine) => cuisine.name !== pillText
        );

        await post(
          "/preferences/remove_preferences_type",
          { uuid: pill.getAttribute("id") },
          undefined,
          undefined,
          false
        );
      } else {
        typesSelected.push(pillText);
        pill.classList.add("selected");
        currentPreferences.cuisine.push({ uuid: pill.getAttribute("id") });

        await post(
          "/preferences/add_preferences_type",
          currentPreferences,
          undefined,
          undefined,
          false
        );
      }
    });
  }
};

document.addEventListener("DOMContentLoaded", () => addImagesToPills());
