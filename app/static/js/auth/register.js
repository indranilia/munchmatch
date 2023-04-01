// Imports
import { post } from "../_api.js";
import { getFormData } from "../_helper.js";

// Get register form from the DOM
const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the register form
    const obj = getFormData(event, registerForm);
    // Try to register with the data from the form
    const { data } = await post("/auth/register", obj);

    const message = encodeURIComponent(data.message);
    window.location.href = `/auth/login?message=${message}`;
  } catch (error) {
    window.location.href = `/auth/login?message=${error.message}`;
  }
});
