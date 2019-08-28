## Generated Story 255706069223404498
* greet
    - utter_greet
* RestaurantSearch
    - utter_ask_location
* RestaurantSearch{"location": "delhi"}
    - slot{"location": "delhi"}
    - utter_ask_cuisine
* RestaurantSearch{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - action_restaurant
    - slot{"location": "delhi"}