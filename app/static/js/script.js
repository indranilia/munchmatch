// DOM
const swiping = document.getElementById('swiping');
const swipe_forward = document.getElementById('swipe_forward');
const swipe_backward = document.getElementById('swipe_backward');

const dishes = [
  {
    imageUrl: 'https://assets.bonappetit.com/photos/57aceacc1b3340441497532d/master/w_2700,h_1621,c_limit/double-rl-ranch-burger.jpg',
    location: '10 Powell Street, 94101',
    rate: 4.5,
    price: '15.99',
    description: 'Beef Burger',
    ingredients: ["Beef Patty", "Brioche Bun", "Cheddar Cheese", "Bacon", "Lettuce", "Tomato", "Onion", "Pickles", "Special Sauce"], 
    reviews: 20

  },
  {
    imageUrl: 'https://www.foodandwine.com/thmb/ZG54SVkYi0x6M4Khc7UqURf_cqE=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/Pan-Fried-Lamb-Dumplings-FT-RECIPE0223-62272815bd454fc6bb25dc3521f6b4eb.jpg',
    location: '1401 Jackson Street, 94119',
    rate: 4.2,
    price: '11.99',
    description: 'Chinese Dumplings', 
    ingredients: ["Flour", "Water", "Eggs", "Scallion", "Chicken", "Salt", "Onion"],
    reviews: 10
  },
  {
    imageUrl: 'https://foodandwine.ie/uploads/article/2019/7/2606/getty_chicken_tikka.jpg',
    location: '1320 McAllister Street, 94107',
    rate: 5.0,
    price: '16.99',
    description: 'Tikka Masala', 
    ingredients: ["Chicken", "Rice", "Tomato", "Butter", "Naan", "Garlic", "Onion", "Spices"], 
    reviews: 120
  },
  {
    imageUrl: 'https://www.giallozafferano.com/images/260-26067/Tiramisu_1200x800.jpg',
    location: '25 Mission Street, 94112',
    rate: 4.0,
    price: '9.99',
    description: 'Traditional Italian Tiramisu', 
    ingredients: ["Coffee", 'Cacao', 'Mascarpone', "Ladyfingers", "Lettuce", "Whipped Cream", 'Vanilla Extract'], 
    reviews: 55
  },
  {
    imageUrl: 'https://www.thespruceeats.com/thmb/N_s7YD61nOB5q_4-T9hl0HwEwvM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/creamy-tomato-pasta-481963-hero-01-da2897ca4ccd4673849c017642e6d827.jpg',
    location: '16th Street, 94102',
    rate: 4.0,
    price: '18.99',
    description: 'Creamy Tomato Pasta', 
    ingredients: ["Pasta", "Whipped Cream", "Beef", "Tomato", "Onion"],
    reviews: 76

  },
];

// variables
let dishCount = 0;

function createDish() {
  const dish = new Dish({
    imageUrl: dishes[dishCount % dishes.length].imageUrl,
    location: dishes[dishCount % dishes.length].location,
    rate: dishes[dishCount % dishes.length].rate,
    price: dishes[dishCount % dishes.length].price,
    description: dishes[dishCount % dishes.length].description, 
    ingredients:  dishes[dishCount % dishes.length].ingredients, 
    reviews:  dishes[dishCount % dishes.length].reviews, 
    onDishDismissed: appendNewDish,

    onDishLiked: () => {
      swipe_forward.style.animationPlayState = 'running';
      swipe_forward.classList.toggle('trigger');
    },
    onDishDisliked: () => {
      swipe_backward.style.animationPlayState = 'running';
      swipe_backward.classList.toggle('trigger');
    }
  });
  swiping.appendChild(dish.element);
  dishCount++;
}

function updateDishes() {
  const dishes = swiping.querySelectorAll('.dish:not(.dismissing)');
  dishes.forEach((dish, index) => {
    dish.style.setProperty('--i', index);
  });
}

function appendNewDish() {
  createDish();
  updateDishes();
}


for (let i = 0; i < dishes.length; i++) {
  createDish();
}
updateDishes();








