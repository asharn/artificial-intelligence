from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json


class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'

    def run(self, dispatcher, tracker, domain):
        config = {"user_key": "6ce88a5ec1419e335afa1c7f92f4b739"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')
        print(loc)
        cuisine = tracker.get_slot('cuisine')
        print(cuisine)
        location_detail = zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat = d1["location_suggestions"][0]["latitude"]
        print(lat)
        lon = d1["location_suggestions"][0]["longitude"]
        print(lon)
        cuisines_dict = {
            'Mexican': 73,
            'Chinese': 25,
            'American': 1,
            'Italian': 55,
            'North Indian': 50,
            'South Indian': 85}
        results = zomato.restaurant_search(
            "sort=rating&order=desc", lat, lon, str(
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

        dispatcher.utter_message("-----\n" + response)
        return [SlotSet('location', loc)]


class ActionSendMail(Action):
    def name(self):
        return 'action_send_mail'

    def run(self, dispatcher, tracker, domain):
        config = {"user_key": "6ce88a5ec1419e335afa1c7f92f4b739"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        location_detail = zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat = d1["location_suggestions"][0]["latitude"]
        lon = d1["location_suggestions"][0]["longitude"]
        cuisines_dict = {
            'Mexican': 73,
            'Chinese': 25,
            'American': 1,
            'Italian': 55,
            'North Indian': 50,
            'South Indian': 85}
        results = zomato.restaurant_search(
            "sort=rating&order=desc", lat, lon, str(
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

        dispatcher.utter_message("-----/n" + response)
        return [SlotSet('location', loc)]
