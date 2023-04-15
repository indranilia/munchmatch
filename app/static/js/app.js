import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import Swipeable from 'react-swipeable';

function TinderForFood() {
  const [currentDishIndex, setCurrentDishIndex] = useState(0);

  const handleSwipeRight = () => {
    setCurrentDishIndex(currentDishIndex + 1);
  };

  const handleSwipeLeft = () => {
    setCurrentDishIndex(currentDishIndex + 1);
  };

  const dishes = [
    {
        id: 1, 
        name: "Pasta Carbonara",
        image: "pasta.jpeg",
        price: "$12.99",
        distance: "1 mile away",
        rating: "4.5"
    },
    {
        id: 2, 
        name: "Spaghetti Bolognese",
        image: "spaghetti.jpeg",
        price: "$10.99",
        distance: "2 miles away",
        rating: "4.0"
    },
    {
        id: 3, 
        name: "Margherita Pizza",
        image: "pizza.jpeg",
        price: "$9.99",
        distance: "3 miles away",
        rating: "4.2"
    }
]

  const currentDish = dishes[currentDishIndex];

  return (
    <div id="swipe-page">
      <div id="dish-box">
        <Swipeable onSwipedRight={handleSwipeRight} onSwipedLeft={handleSwipeLeft}>
          <img src={currentDish.image} alt={currentDish.name} />
        </Swipeable>
        <h2>{currentDish.name}</h2>
        <p>{currentDish.price}</p>
        <span>{currentDish.distance} | {currentDish.rating} rating</span>
        <div>
          <button className="check-button" onClick={handleSwipeRight}></button>
          <button className="info-button"></button>
          <button className="ex-button" onClick={handleSwipeLeft}></button>
        </div>
      </div>
    </div>
  );
}

ReactDOM.render(<TinderForFood />, document.getElementById('root'));
