import { remove } from "../_api.js";
import { getImageFromGoogleImages } from "../integrations/google.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

const munchImages = document.getElementsByClassName("munch-image");
const munches = document.getElementsByClassName("matched_dish");

const loadMatchesImages = async () => {
  for (const image of munchImages) {
    if (image.getAttribute("src") === "None") {
      const newSrc = await getImageFromGoogleImages(
        image.getAttribute("alt"),
        undefined,
        false
      );
      image.src = newSrc;
    }
  }
};

const loadMunches = async () => {
  for (const munch of munches) {
    const deleteButton = munch.querySelector(".delete-btn");
    deleteButton.addEventListener("click", async () => {
      try {
        const status = await remove(
          "/munches",
          munch.getAttribute("id"),
          undefined,
          undefined,
          false
        );
        if (status === 204) {
          munch.remove();
          successToast("Munch deleted successfully");
          return;
        }

        errorToast("Something went wrong. Please try again");
      } catch (error) {
        errorToast("Something went wrong. Please try again");
      }
    });
  }
};

loadMatchesImages();
loadMunches();
