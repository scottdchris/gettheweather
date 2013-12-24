#!/python/bin/python3.3
"""
Get The Weather App by Christopher Scott
http://www.scottdchris.com/

"""
from twython import Twython
import django
from bs4 import BeautifulSoup
import pprint		#Pretty Print
import json
import requests		#Requests
import re 			#Regular Expressions
import time

#Twython OAuth 1 Authentication
APP_KEY		= #Removed for git
APP_SECRET	= #Removed for git
OAUTH_TOKEN = #Removed for git
OAUTH_TOKEN_SECRET = #Removed for git

#Global variables
IDFile = open('mentionID.txt', 'r+')

'''
checkWeather method returns a dictionary with various weather attributes
@param str of coordinates
@return dict of weather attributes
'''
def checkWeather(rawCoordinates):
	#Get the JSON with r.json()
	coordinates =  str(rawCoordinates[1]) + ',' + str(rawCoordinates[0])
	parsed_json = requests.get('http://api.wunderground.com/api/877bcd60d1e8fa67/forecast/conditions/geolookup/q/%s.json' % (coordinates)).json()
	#pprint.pprint(parsed_json)
	location = parsed_json['location']['city']
	temp = parsed_json['current_observation']['temp_f']
	weather = parsed_json['current_observation']['weather']
	high = parsed_json['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
	low = parsed_json['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
	feelsLike = parsed_json['current_observation']['feelslike_string']
	#chanceOfRain = parsed_json['']
	forecast = parsed_json['forecast']['txt_forecast']['forecastday'][0]['fcttext']

	weather = {
	'location' : location,
	'temp' : temp,
	'weather' : weather,
	'high' : high,
	'low' : low,
	'feelsLike' : feelsLike,
	'forecast' : forecast
	#'chanceOfRain' : chanceOfRain,
	}

	return weather

def createTweet(mention):
	user_handle = '@' + mention['user']['screen_name']
	if mention['place'] == None:
		tweet = "Hey %s, you forgot to add your location to your tweet!" % (user_handle)
	else:
		currentWeather = checkWeather(mention['place']['bounding_box']['coordinates'][0][0])
		tweet = "%s Here's today's weather in %s: It's currently %s and %s with a high of %s and a low of %s." % (user_handle, currentWeather['location'], currentWeather['temp'], currentWeather['weather'], currentWeather['high'], currentWeather['low'])
	return tweet

#Returns true or false depending on if the latest tweet has been responded to already
def newMention(newestMention):	#takes one mention object as a parameter
	for line in IDFile:
		if newestMention['id_str']+'\n' == line:
			return False
	return True

def main():
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	mentions = twitter.get_mentions_timeline()
	if newMention(mentions[0]):
		IDFile.write(mentions[0]['id_str']+'\n')
		#pprint.pprint(mentions[0])
		tweet = createTweet(mentions[0])
		print("@GetTheWeather just tweeted the following:")
		print(tweet)
		twitter.update_status(status=tweet)

time.sleep(1) #Script runs once every 1:01 mins to avoid Twitter API Rate Limit Error of 15 calls per 15 minutes
main()
IDFile.close()
print('run successfully')
