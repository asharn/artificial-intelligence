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
import codecs
LOG_FILENAME = 'out.log'
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
	MAIL_PASSWORD = codecs.decode('qi@123YC', 'rot_13')
	)
mail = Mail(app)

class ActionCheckServingCity(Action):
    def name(self):
        return 'action_city_match'

    def run(self, dispatcher, tracker, domain):
        tierFirst = ['bangalore', 'chennai', 'new delhi', 'hyderabad', 'kolkata', 'mumbai', 'ahmedabad', 'pune']
        tierSecond = ['agra', 'ajmer', 'aligarh', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bokaro steel city', 'chandigarh', 'nagpur', 'cuttack', 'dehradun', 'dhanbad', 'bhilai', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur', 'gulbarga', 'guntur', 'gwalior', 'gurgaon', 'guwahati', 'hubli–dharwad', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kakinada', 'kannur', 'kanpur', 'kochi', 'kottayam', 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'ludhiana', 'lucknow', 'madurai', 'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 'pondicherry', 'allahabad', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur', 'srinagar', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tirupati', 'tirunelveli', 'tiruppur', 'tiruvannamalai', 'ujjain', 'bijapur', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'vellore', 'warangal', 'surat', 'visakhapatnam', 'coimbatore' ]
        consolidatedTierIstAndSecondCities = tierFirst + tierSecond
        loc = tracker.get_slot('city').lower()
        logger.info("Checking city is covered by Zomato or not. -> Location is : " + loc)
        #logger.info(str(domain))
        flag = True
        if(loc not in consolidatedTierIstAndSecondCities):
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
        priceSlot = tracker.get_slot('price')
        logger.info("Type of Price Slot is : " + str(type(priceSlot)))
        logger.info("Price Slot is : "+priceSlot)
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
                cuisines_dict.get(cuisine)), 1000)
        d = json.loads(results)
        response = ""
        if d['results_found'] == 0:
            dispatcher.utter_template("utter_sorry_dont_operate", tracker)
        else:
            counter = 0
            for restaurant in d['restaurants']:
                averageCostOfTwoPerson = restaurant['restaurant']['average_cost_for_two']
                if(counter >= 5):
                    break
                if(priceSlot == "1" and averageCostOfTwoPerson <=300 ):
                    counter = counter + 1
                    response += str(counter) + ". "
                    response += restaurant['restaurant']['name']
                    response += " in " 
                    response += restaurant['restaurant']['location']['address']
                    response += " has been rated " 
                    response += restaurant['restaurant']['user_rating']['aggregate_rating'] 
                    response += ".\n\n"
                elif(priceSlot == "2" and averageCostOfTwoPerson >300 and  averageCostOfTwoPerson <=700):
                    counter = counter + 1
                    response += str(counter) + ". "
                    response += restaurant['restaurant']['name']
                    response += " in " 
                    response += restaurant['restaurant']['location']['address']
                    response += " has been rated " 
                    response += restaurant['restaurant']['user_rating']['aggregate_rating'] 
                    response += ".\n\n"
                elif(priceSlot == "3" and averageCostOfTwoPerson > 700):
                    counter = counter + 1
                    response += str(counter) + ". "
                    response += restaurant['restaurant']['name']
                    response += " in " 
                    response += restaurant['restaurant']['location']['address']
                    response += " has been rated " 
                    response += restaurant['restaurant']['user_rating']['aggregate_rating'] 
                    response += ".\n\n"
            if(response == ""):
                response+='There is not any restaurant in that budget. Please search by some other options.'
            logger.info("Response is : "+response)
            dispatcher.utter_message("\n-----\n" + response)
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
                cuisines_dict.get(cuisine)), 10)
        d = json.loads(results)
        response = ""
        if d['results_found'] == 0:
            response = "no results"
        else:
            counter = 0
            for restaurant in d['restaurants']:
                counter += 1
                response += str(counter) + ". "
                response += '<b>'
                response += restaurant['restaurant']['name']
                response += '</b>'
                response += " in "
                response += '<b>'
                response += restaurant['restaurant']['location']['address']
                response += '</b>'
                response += " with an average budget of two people Rs."
                response += '<b>'
                response += str(restaurant['restaurant']['average_cost_for_two'])
                response += '</b>'
                response += " has been rated "
                response += '<b>'
                response += restaurant['restaurant']['user_rating']['aggregate_rating'] 
                response += '</b>'
                response += ".\n"
            msg = Message("Hi, Your search result for top Restaurants !",
            sender="dvlpmailsender@gmail.com",
            recipients=[emailId])
            msg.body = response
            with app.app_context():
                mail.send(msg)
        #dispatcher.utter_message("-----\n" + response)
        return [SlotSet('city', loc)]
