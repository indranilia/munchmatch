// Get the elements that we need to manipulate
const pictureContainer = document.querySelector(".picture-container");
const usernameSpan = document.querySelector("#username");
const nameSpan = document.querySelector("#name");
const emailSpan = document.querySelector("#email");
const editForm = document.querySelector("#edit-form");
const editValueInput = document.querySelector("#edit-value");

// Define a function that will be called when the "Edit" button is clicked
function editField(fieldName) {
  // Show the edit form and set its value to the current value of the field
  editForm.style.display = "block";
  switch (fieldName) {
    case "picture":
      editValueInput.value = pictureContainer.querySelector("img").getAttribute("src");
      break;
    case "username":
      editValueInput.value = usernameSpan.textContent;
      break;
    case "name":
      editValueInput.value = nameSpan.textContent;
      break;
    case "email":
      editValueInput.value = emailSpan.textContent;
      break;
  }
}

// Define a function that will be called when the "Cancel" button is clicked
function cancelEdit() {
  // Hide the edit form and clear its value
  editForm.style.display = "none";
  editValueInput.value = "";
}

// Define a function that will be called when the "Save" button is clicked
function submitEdit() {
  // Get the current value of the input field
  const newValue = editValueInput.value;

  // Determine which field we are editing based on the ID of the input field
  switch (editValueInput.id) {
    case "edit-value-picture":
      pictureContainer.querySelector("img").setAttribute("src", newValue);
      break;
    case "edit-value-username":
      usernameSpan.textContent = newValue;
      break;
    case "edit-value-name":
      nameSpan.textContent = newValue;
      break;
    case "edit-value-email":
      emailSpan.textContent = newValue;
      break;
  }

  // Hide the edit form and clear its value
  editForm.style.display = "none";
  editValueInput.value = "";
}
