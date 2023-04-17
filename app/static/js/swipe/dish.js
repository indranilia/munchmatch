class Dish {
  constructor({ picture, price, name, location, onDishLiked, onDishDisliked }) {
    this.picture = picture;
    this.location = location;
    // this.rate = rate;
    this.price = price;
    this.name = name;
    // this.ingredients = ingredients;
    // this.reviews = reviews;
    this.onDishLiked = onDishLiked;
    this.onDishDisliked = onDishDisliked;
    this.#init();
  }

  #startPoint;
  #offsetX;
  #offsetY;

  #isTouchDevice = () => {
    return (
      "ontouchstart" in window ||
      navigator.maxTouchPoints > 0 ||
      navigator.msMaxTouchPoints > 0
    );
  };

  #init = () => {
    const dish = document.createElement("div");
    dish.classList.add("dish");
    dish.style.background = "#F2CF53";

    const imgContainer = document.createElement("div");
    imgContainer.classList.add("img-container");

    const img = document.createElement("img");
    img.src = this.picture;
    img.style.display = "block";
    img.style.margin = "auto";
    img.style.height = "100%";
    imgContainer.append(img);
    dish.append(imgContainer);

    const infoContainer = document.createElement("div");
    infoContainer.classList.add("info-container");
    // infoContainer.style.display = 'flex';
    infoContainer.style.flexDirection = "row";
    infoContainer.style.alignItems = "center";
    infoContainer.style.justifyContent = "space-between";

    const nameAndPrice = document.createElement("div");
    nameAndPrice.style.display = "flex";
    nameAndPrice.style.flexDirection = "row";

    function generateDollarSigns(price) {
      if (price <= 10) {
        return '<span style="color:#000;">$</span>';
      } else if (price <= 15) {
        return '<span style="color:#000;">$$</span>';
      } else if (price <= 20) {
        return '<span style="color:#000;">$$$</span>';
      } else {
        return '<span style="color:#000;">$$$$</span>';
      }
    }

    const name = document.createElement("div");
    name.style.fontSize = "24px";
    name.style.color = "black";

    name.innerHTML = `${this.name} ${generateDollarSigns(this.price)}`;
    nameAndPrice.append(name);

    const price = document.createElement("div");
    price.textContent = "$" + this.price;
    price.style.marginLeft = "auto";
    price.style.color = "#c91818";
    nameAndPrice.append(price);
    infoContainer.append(nameAndPrice);

    const rateAndAddress = document.createElement("div");
    rateAndAddress.classList.add("rate-container");

    // const rate = document.createElement('div');
    // let stars = '';
    // for (let i = 0; i < this.rate; i++) {
    // stars += '★';
    // }
    // rate.textContent = this.rate + " : " + stars + "(" + this.reviews + ")";
    // rateContainer.append(rate);

    // rateAndAddress.append(rateContainer);

    if (this.location) {
      const address = document.createElement("div");
      address.textContent = "📍 " + this.location;
      rateAndAddress.append(address);
      infoContainer.append(rateAndAddress);
    }

    // create the View on Google Maps button container
    const mapsContainer = document.createElement("div");
    mapsContainer.style.display = "flex";
    mapsContainer.style.flexDirection = "column";
    mapsContainer.style.alignItems = "center";

    const viewOnGoogleMapsButton = document.createElement("div");
    viewOnGoogleMapsButton.textContent = "View on Google Maps";
    viewOnGoogleMapsButton.classList.add("maps-button");
    viewOnGoogleMapsButton.addEventListener("click", () => {
      const mapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
        this.location || this.name
      )}`;
      window.open(mapsUrl, "_blank");
    });
    mapsContainer.append(viewOnGoogleMapsButton);

    // const ingredientsButton = document.createElement('button');
    // ingredientsButton.classList.add('ingredients-button');
    // ingredientsButton.addEventListener('click', () => {
    //   if (ingredientsContainer.style.display === 'none') {
    //     ingredientsContainer.style.display = 'block';
    //     ingredientsContainer.style.background = 'white';
    //     ingredientsContainer.style.borderRadius = '20px';
    //     imgContainer.style.display = 'none';
    //     infoContainer.style.display = 'none';
    //   } else {
    //     ingredientsContainer.style.display = 'none';
    //     imgContainer.style.display = 'block';
    //     infoContainer.style.display = 'block';
    //   }
    // });

    // const ingredientsContainer = document.createElement('div');
    // ingredientsContainer.classList.add('ingredients-container');
    // ingredientsContainer.style.display = 'none';

    // const ingredientsTitle = document.createElement('div');
    // ingredientsTitle.textContent = 'Ingredients 🧑‍🍳';
    // ingredientsTitle.style.fontStyle = 'italic';
    // ingredientsContainer.append(ingredientsTitle);

    // const ingredientsList = document.createElement('div');
    // const ingredientsText = document.createTextNode(`${this.ingredients.join(', ')}`);
    // ingredientsList.appendChild(ingredientsText);
    // ingredientsContainer.append(ingredientsList);

    this.element = dish;
    // dish.append(ingredientsButton);
    // dish.append(ingredientsContainer);
    dish.append(infoContainer);
    dish.append(mapsContainer);

    if (this.#isTouchDevice()) {
      this.#listenToTouchEvents();
    } else {
      this.#listenToMouseEvents();
    }
  };

  #listenToTouchEvents = () => {
    this.element.addEventListener("touchstart", (e) => {
      const touch = e.changedTouches[0];
      if (!touch) return;
      const { clientX, clientY } = touch;
      this.#startPoint = { x: clientX, y: clientY };
      document.addEventListener("touchmove", this.#handleTouchMove);
      this.element.style.transition = "transform 0s";
    });

    document.addEventListener("touchend", this.#handleTouchEnd);
    document.addEventListener("cancel", this.#handleTouchEnd);
  };

  #listenToMouseEvents = () => {
    this.element.addEventListener("mousedown", (e) => {
      const { clientX, clientY } = e;
      this.#startPoint = { x: clientX, y: clientY };
      document.addEventListener("mousemove", this.#handleMouseMove);
      this.element.style.transition = "transform 0s";
    });

    document.addEventListener("mouseup", this.#handleMoveUp);

    // prevent card from being dragged
    this.element.addEventListener("dragstart", (e) => {
      e.preventDefault();
    });
  };

  #handleMove = (x, y) => {
    this.#offsetX = x - this.#startPoint.x;
    this.#offsetY = y - this.#startPoint.y;
    const rotate = this.#offsetX * 0.1;
    this.element.style.transform = `translate(${this.#offsetX}px, ${
      this.#offsetY
    }px) rotate(${rotate}deg)`;
    // dismiss card
    if (Math.abs(this.#offsetX) > this.element.clientWidth * 0.7) {
      this.#dismiss(this.#offsetX > 0 ? 1 : -1);
    }
  };

  // mouse event handlers
  #handleMouseMove = (e) => {
    e.preventDefault();
    if (!this.#startPoint) return;
    const { clientX, clientY } = e;
    this.#handleMove(clientX, clientY);
  };

  #handleMoveUp = () => {
    this.#startPoint = null;
    document.removeEventListener("mousemove", this.#handleMouseMove);
    this.element.style.transform = "";
  };

  // touch event handlers
  #handleTouchMove = (e) => {
    if (!this.#startPoint) return;
    const touch = e.changedTouches[0];
    if (!touch) return;
    const { clientX, clientY } = touch;
    this.#handleMove(clientX, clientY);
  };

  #handleTouchEnd = () => {
    this.#startPoint = null;
    document.removeEventListener("touchmove", this.#handleTouchMove);
    this.element.style.transform = "";
  };

  #dismiss = (direction) => {
    this.#startPoint = null;
    document.removeEventListener("mouseup", this.#handleMoveUp);
    document.removeEventListener("mousemove", this.#handleMouseMove);
    document.removeEventListener("touchend", this.#handleTouchEnd);
    document.removeEventListener("touchmove", this.#handleTouchMove);
    this.element.style.transition = "transform 1s";
    this.element.style.transform = `translate(${
      direction * window.innerWidth
    }px, ${this.#offsetY}px) rotate(${90 * direction}deg)`;
    this.element.classList.add("dismissing");
    setTimeout(() => {
      this.element.remove();
    }, 1000);

    if (typeof this.onDishLiked === "function" && direction === 1) {
      this.onDishLiked();
    }
    if (typeof this.onDishDisliked === "function" && direction === -1) {
      this.onDishDisliked();
    }
  };
}
