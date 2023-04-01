// Imports
import { post } from "../_api.js";
import { getFormData } from "../_helper.js";

// Get forgot password form form from the DOM
const forgotPasswordForm = document.getElementById("forgot-password-form");

forgotPasswordForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the form
    const obj = getFormData(event, forgotPasswordForm);

    // Try to login with the data from the form
    const { data } = await post("/auth/forgot-password", obj);

    const message = encodeURIComponent(data.message);
    window.location.href = `/auth/login?message=${message}`;
  } catch (error) {
    window.location.href = `/auth/login?message=${error.message}`;
  }
});
