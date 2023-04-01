// Imports
import { post } from "../_api.js";
import { getFormData } from "../_helper.js";

// Get login form from the DOM
const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the login form
    const obj = getFormData(event, loginForm);

    // Try to login with the data from the form
    const { status, data } = await post("/auth/login", obj, undefined, false);

    if (status === 200) {
      window.location.href = "/home";
      return;
    }

    const message = encodeURIComponent(data.message);
    window.location.href = `/auth/login?message=${message}`;
  } catch (error) {
    window.location.href = `/auth/login?message=${error.message}`;
  }
});
