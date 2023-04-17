export async function successModal(text, callback = () => {}) {
  Swal.fire({
    title: "Success",
    text,
    confirmButtonColor: "#FE760D",
    icon: "success",
    heightAuto: false,
  }).then(callback);
}

export async function errorModal(
  text,
  callback = () => {},
  confirmButtonText = "Ok"
) {
  Swal.fire({
    title: "Error",
    text,
    confirmButtonColor: "#FE760D",
    confirmButtonText,
    icon: "error",
    heightAuto: false,
  }).then(callback);
}

export async function warningModal(text, callback = () => {}) {
  Swal.fire({
    title: "Warning",
    text,
    confirmButtonColor: "#FE760D",
    icon: "warning",
    heightAuto: false,
  }).then(callback);
}

export async function successToast(text) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-right",
    iconColor: "white",
    customClass: {
      popup: "colored-toast",
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
  });
  await Toast.fire({
    icon: "success",
    title: text,
  });
}

export async function errorToast(text) {
  const Toast = Swal.mixin({
    toast: true,
    position: "top-right",
    iconColor: "white",
    customClass: {
      popup: "colored-toast",
    },
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
  });
  await Toast.fire({
    icon: "error",
    title: text,
  });
}
