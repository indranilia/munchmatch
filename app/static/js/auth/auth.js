import { showLogin, showRegister } from "./authHelper.js";

document.querySelector("#linkCreateAccount").addEventListener("click", (e) => {
  e.preventDefault();
  showRegister();
});

document.querySelector("#linkLogin").addEventListener("click", (e) => {
  e.preventDefault();
  showLogin();
});
