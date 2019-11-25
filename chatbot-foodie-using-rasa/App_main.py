from flask import session,flash
import pandas as pd
import numpy as np 
from flask import Response
import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import tempfile
import simplejson as j
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import json
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from flask_mail import Mail, Message
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'dvlpmailsender@gmail.com',
	MAIL_PASSWORD = 'real_password'
	)
mail = Mail(app)   

tierFirst = ['bangalore', 'chennai', 'delhi', 'hyderabad', 'kolkata', 'mumbai', 'ahmedabad', 'pune']
tierSecond = ['agra', 'ajmer', 'aligarh', 'amravati', 'amritsar', 'asansol', 'aurangabad', 'bareilly', 'belgaum', 'bhavnagar', 'bhiwandi', 'bhopal', 'bhubaneswar', 'bikaner', 'bokaro steel city', 'chandigarh', 'nagpur', 'cuttack', 'dehradun', 'dhanbad', 'bhilai', 'durgapur', 'erode', 'faridabad', 'firozabad', 'ghaziabad', 'gorakhpur', 'gulbarga', 'guntur', 'gwalior', 'gurgaon', 'guwahati', 'hubli–dharwad', 'indore', 'jabalpur', 'jaipur', 'jalandhar', 'jammu', 'jamnagar', 'jamshedpur', 'jhansi', 'jodhpur', 'kakinada', 'kannur', 'kanpur', 'kochi', 'kottayam', 'kolhapur', 'kollam', 'kota', 'kozhikode', 'kurnool', 'ludhiana', 'lucknow', 'madurai', 'malappuram', 'mathura', 'goa', 'mangalore', 'meerut', 'moradabad', 'mysore', 'nanded', 'nashik', 'nellore', 'noida', 'palakkad', 'patna', 'pondicherry', 'allahabad', 'raipur', 'rajkot', 'rajahmundry', 'ranchi', 'rourkela', 'salem', 'sangli', 'siliguri', 'solapur', 'srinagar', 'thiruvananthapuram', 'thrissur', 'tiruchirappalli', 'tirupati', 'tirunelveli', 'tiruppur', 'tiruvannamalai', 'ujjain', 'bijapur', 'vadodara', 'varanasi', 'vasai-virar city', 'vijayawada', 'vellore', 'warangal', 'surat', 'visakhapatnam', 'coimbatore' ]
@app.route('/style.css')
def fetchCss():
    return render_template('style.css')

@app.route('/script.js')
def fetchJs():
    return render_template('script.js')

@app.route('/_config.yml')
def fetchConfig():
    return render_template('/_config.yml')


@app.route('/')
def index():
    return render_template('index.html')
    
    
interpreter = Interpreter.load('./models/nlu/default/restaurantnlu')
@app.route('/user_text_parsing', methods=['POST'])
def transform():
    print('Rest called outside') 
    if request.headers['Content-Type'] == 'application/json':   
        query = request.json.get("user-utter")
        results=interpreter.parse(query)
        js = '{"message":"In which city are you looking for restaurants?"}'
        print(results) 
        #This condition goes to story.md file to interract with chat bot.
        if('RestaurantSearch' == results['intent']['name']):
                print(results['entities'])  
                for entity in results['entities']:
                        print(entity['entity']) 
                        if('city' == entity['entity']
                           and (entity['value'] in tierFirst
                                or entity['value'] in tierSecond)):
                                      js = '{"message":"What kind of cuisine would you prefer?'
                                      js += '<ul>'
                                      js += '<li>Chinese</li>'
                                      js += '<li>Mexican</li>'
                                      js += '<li>Italian</li>'
                                      js += '<li>American</li>'
                                      js += '<li>South Indian</li>'
                                      js += '<li>North Indian</li>'
                                      js += '</ul>'  
                                      js += '"}'
                        else:
                            js = '{"message":"We do not operate in that area yet."}'    
        elif('cuisinetype' == results['intent']['name']):
                js = '{"message":"What price range are you looking at?'
                js += '<ul>'
                js += '<li>Lesser than Rs. 300</li>'
                js += '<li>Rs. 300 to 700</li>'
                js += '<li>More than 700</li>'
                js += '</ul>'
                js += '"}'
        elif('budget' == results['intent']['name']):
                js = '{"message":"Here is you search result!!!'
                js += '<ul>'
                js += '<li>{restaurant_name_1} in {restaurant_address_1} has been rated {rating}.</li>'
                js += '<li>{restaurant_name_2} in {restaurant_address_2} has been rated {rating}.</li>'
                js += '<li>{restaurant_name_3} in {restaurant_address_3} has been rated {rating}.</li>'
                js += '<li>{restaurant_name_4} in {restaurant_address_4} has been rated {rating}.</li>'
                js += '<li>{restaurant_name_5} in {restaurant_address_5} has been rated {rating}.</li>'
                js += '</ul>'
                js += 'Would you like to know top 10 restaurant on your mail.'
                js += '"}'
        elif('sendemail' == results['intent']['name']):
                js = '{"message":"Please, provide your email id."}'
        elif('bye' == results['intent']['name']):
                js = '{"message":"goodbye"}'
        else:
                js = '{"message":"I am still learning. I do not understand."}'
        #print(js) ``
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/send-mail', methods=['POST'])
def sendMail():
        if request.headers['Content-Type'] == 'application/json':
                try:
                        recipientEmail = request.json.get("email")
                        restaurants = request.json.get("top-10-restaurants")
                        msg = Message("Hi, Your search result for top 10 Restaurants!",
                                sender="dvlpmailsender@gmail.com",
                                recipients=[recipientEmail])
                        msg.body = restaurants
                        mail.send(msg)
                        return 'Mail sent successfully'
                except Exception as e:
                        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
