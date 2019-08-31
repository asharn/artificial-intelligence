## User not interested
* greet
    - utter_greet
* deny
    - utter_goodbye

## Generated Story 1
* greet
    - utter_greet
* RestaurantSearch
    - utter_ask_location
* RestaurantSearch{"city": "New Delhi"}
    - slot{"city": "New Delhi"}
    - action_city_match
    - slot{"city_match": "True"}
    - utter_ask_cuisine
* cuisinetype{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_budget
* budget{"price": "500"}
    - slot{"price": "500"}
    - utter_searching
    - action_restaurant
    - utter_ask_for_email_to_send
* affirm
    - utter_ask_email_address
* SendMail{"email": "er.ashishkarn@gmail.com"}
    - slot{"email": "er.ashishkarn@gmail.com"}
    - action_send_mail
    - slot{"city": "New Delhi"}
    - utter_goodbye
* bye
    - export


