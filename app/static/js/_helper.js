const validateForm = (obj) => {
  // Check if all keys inside the obj have a non-empty value
  for (const key of Object.keys(obj)) {
    if (`${obj[key]}`.trim() === "") {
      return false;
    }
  }

  return true;
};

// Get data from form to send to backend
export function getFormData(event, formHTMLElement) {
  event.preventDefault(); // Prevents the form to submit its default action

  // Gets the value of all inputs and textareas inside the form
  const inputs = formHTMLElement.getElementsByTagName("input");
  const textareas = formHTMLElement.getElementsByTagName("textarea");
  const obj = {};

  for (const input of inputs) {
    obj[input.name] = input.value;
  }

  for (const textarea of textareas) {
    obj[textarea.name] = textarea.value;
  }

  // Validate if all inputs/textareas inside the form are filled
  if (validateForm(obj)) {
    return obj;
  } else {
    throw new Error("Please, fill all the information");
  }
}

// Create loading overlay to process data
export function createLoading() {
  // Creating container
  const loadingContainer = document.createElement("div");
  loadingContainer.id = "loading-container";
  loadingContainer.classList.add("modal-container");
  loadingContainer.style.zIndex = 100;
  loadingContainer.style.display = "flex";

  // Creating spinner
  const mainSpinner = document.createElement("div");
  mainSpinner.classList.add("spinner");
  for (let i = 0; i < 12; i++) {
    const spinBar = document.createElement("div");
    mainSpinner.appendChild(spinBar);
  }

  loadingContainer.appendChild(mainSpinner);

  // Adding overlay to page
  document.body.appendChild(loadingContainer);
}

// Remove loading overlay after processing data
export function removeLoading() {
  const loadingContainer = document.getElementById("loading-container");
  loadingContainer.remove();
}
