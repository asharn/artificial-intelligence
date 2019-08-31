from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json
import logging

# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from flask_mail import Mail, Message
from flask import Flask
LOG_FILENAME = 'app.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.app_context()
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'dvlpmailsender@gmail.com',
	MAIL_PASSWORD = 'dv@123LP'
	)
with app.app_context():
    mail = Mail(app)

class ActionCheckServingCity(Action):
    def name(self):
        return 'action_city_match'

    def run(self, dispatcher, tracker, domain):
        tierFirst = ['bangalore', 'chennai', 'new delhi', 'hyderabad', 'kolkata', 'mumbai', 'ahmedabad', 'pune']
        tierSecond = ['agra', 'ajmer', 'aligarh', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bokaro steel city', 'chandigarh', 'nagpur', 'cuttack', 'dehradun', 'dhanbad', 'bhilai', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur', 'gulbarga', 'guntur', 'gwalior', 'gurgaon', 'guwahati', 'hubli–dharwad', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kakinada', 'kannur', 'kanpur', 'kochi', 'kottayam', 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'ludhiana', 'lucknow', 'madurai', 'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 'pondicherry', 'allahabad', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur', 'srinagar', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tirupati', 'tirunelveli', 'tiruppur', 'tiruvannamalai', 'ujjain', 'bijapur', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'vellore', 'warangal', 'surat', 'visakhapatnam', 'coimbatore' ]
        loc = tracker.get_slot('city').lower()
        logger.info("Checking city is covered by Zomato or not. -> Location is : " + loc)
        logger.info(str(domain))
        flag = True
        if(loc not in tierFirst and loc not in tierSecond):
            dispatcher.utter_template("utter_sorry_dont_operate", tracker)
            flag = False
        return [SlotSet('city_match', flag)]
        

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'

    def run(self, dispatcher, tracker, domain):
        config = {"user_key": "6ce88a5ec1419e335afa1c7f92f4b739"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('city').lower()
        logger.info("Location is : "+loc)
        cuisine = tracker.get_slot('cuisine').lower()
        logger.info("Cuisine is : "+cuisine)
        location_detail = zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat = d1["location_suggestions"][0]["latitude"]
        logger.info("Latitude is : "+str(lat))
        lon = d1["location_suggestions"][0]["longitude"]
        logger.info("Longitude is : " + str(lon))
        cuisines_dict = {
            'Mexican': 73,
            'Chinese': 25,
            'American': 1,
            'Italian': 55,
            'North Indian': 50,
            'South Indian': 85}
        results = zomato.restaurant_search(
            "&sort=rating&order=desc", lat, lon, str(
                cuisines_dict.get(cuisine)), 5)
        d = json.loads(results)
        response = ""
        if d['results_found'] == 0:
            response = "We do not operate in that area yet"
        else:
            for restaurant in d['restaurants']:
                response += "Found " + restaurant['restaurant']['name']
                response += " in " + \
                    restaurant['restaurant']['location']['address']
                response += " has been rated " + \
                    restaurant['restaurant']['user_rating']['aggregate_rating'] + ".\n"
        logger.info("Response is : "+response)
        dispatcher.utter_message("-----\n" + response)
        return [SlotSet('city', loc)]


class ActionSendMail(Action):
    def name(self):
        return 'action_send_mail'

    def run(self, dispatcher, tracker, domain):
        config = {"user_key": "6ce88a5ec1419e335afa1c7f92f4b739"}
        zomato = zomatopy.initialize_app(config)
        emailId = tracker.get_slot('email')
        loc = tracker.get_slot('city')
        cuisine = tracker.get_slot('cuisine')
        location_detail = zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat = d1["location_suggestions"][0]["latitude"]
        lon = d1["location_suggestions"][0]["longitude"]
        cuisines_dict = {
            'mexican': 73,
            'chinese': 25,
            'american': 1,
            'italian': 55,
            'north Indian': 50,
            'south Indian': 85}
        results = zomato.restaurant_search(
            "&sort=rating&order=desc", lat, lon, str(
                cuisines_dict.get(cuisine)), 5)
        d = json.loads(results)
        response = ""
        if d['results_found'] == 0:
            response = "no results"
        else:
            for restaurant in d['restaurants']:
                response += "Found " + restaurant['restaurant']['name']
                response += " in " + \
                    restaurant['restaurant']['location']['address']
                response += " has been rated " + \
                    restaurant['restaurant']['user_rating']['aggregate_rating'] + ".\n"
            msg = Message("Hi, Your search result for top Restaurants !",
            sender="dvlpmailsender@gmail.com",
            recipients=[emailId])
            msg.body = response
            mail.send(msg)
        dispatcher.utter_message("-----\n" + response)
        return [SlotSet('city', loc)]
