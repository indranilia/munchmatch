import { patch } from "../_api.js";
import { errorToast, successToast } from "../integrations/sweetAlert.js";

// Get the elements that we need to manipulate
const nameEditButton = document.querySelector("#edit-name-button");
const emailEditButton = document.querySelector("#edit-email-button");
const nameEditInput = document.querySelector("#edit-name-input");
const emailEditInput = document.querySelector("#edit-email-input");
const nameValue = document.querySelector("#name-value");
const emailValue = document.querySelector("#email-value");
const mainNameValue = document.querySelector("#main-name-value");
const mainEmailValue = document.querySelector("#main-email-value");

const saveSettings = async (body) => {
  if (body.email && body.name) {
    try {
      const status = await patch("/account", body);

      if (status === 204) {
        successToast("Account updated successfully!");
        return true;
      }

      errorToast("Something went wrong. Please try again");
      return false;
    } catch (error) {
      errorToast(error.message);
      return false;
    }
  } else {
    errorToast("Please fill the email and password");
    return false;
  }
};

nameEditButton.addEventListener("click", () => {
  if (nameEditButton.innerHTML === "Edit") {
    nameEditInput.classList.remove("hidden");
    nameValue.classList.add("hidden");
    nameEditButton.innerHTML = "Save";
  } else {
    if (
      saveSettings({ email: emailEditInput.value, name: nameEditInput.value })
    ) {
      nameValue.innerHTML = mainNameValue.innerHTML = nameEditInput.value;
      nameEditInput.classList.add("hidden");
      nameValue.classList.remove("hidden");
      nameEditButton.innerHTML = "Edit";
    }
  }
});

emailEditButton.addEventListener("click", () => {
  if (emailEditButton.innerHTML === "Edit") {
    emailEditInput.classList.remove("hidden");
    emailValue.classList.add("hidden");
    emailEditButton.innerHTML = "Save";
  } else {
    if (
      saveSettings({ email: emailEditInput.value, name: nameEditInput.value })
    ) {
      emailValue.innerHTML = mainEmailValue.innerHTML = emailEditInput.value;
      emailEditInput.classList.add("hidden");
      emailValue.classList.remove("hidden");
      emailEditButton.innerHTML = "Edit";
    }
  }
});
