// Imports
import { patch } from "../_api.js";
import { getFormData } from "../_helper.js";

// Get forgot password form form from the DOM
const resetPasswordForm = document.getElementById("reset-password-form");

resetPasswordForm.addEventListener("submit", async (event) => {
  // If the try doesn't pass, the user didn't fill all the information
  try {
    // Get data of the form
    const obj = getFormData(event, resetPasswordForm);

    // Try to reset password with the data from the form
    await patch(window.location.href, obj, true);

    window.location.href = `/auth/login`;
  } catch (error) {
    window.location.href = `/auth/login?message=${error.message}`;
  }
});
