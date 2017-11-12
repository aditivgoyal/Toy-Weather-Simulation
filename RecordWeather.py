import os
import json
import datetime
import requests

import pandas
import forecastio


'''
This function get_location_info() is designed to return the longitude, latitude and elevation of all the cities
It takes a single argument:
list_of_locations - It is the list having names of all the cities
'''
def get_location_info(list_of_locations):

    #url to find the longitude and the latitude of the city   
    geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address='

    #url to find the elevation of the city ie how many metres above the sea level
    elevation_url = 'https://maps.googleapis.com/maps/api/elevation/json?locations='

    location_info_list = []

    for location in list_of_locations:
        location_info = {'location': location}

        r = requests.get(geocode_url+location).json()
        if r.get('results'):
            for positions_results in r.get('results'):
                position = positions_results.get('geometry','').get('location','')
                location_info['latitude'] = position.get('lat','')
                location_info['latitude'] = round(location_info['latitude'],2) #rounding the value upto 2 decimal points
                
                location_info['longitude'] = position.get('lng','')
                location_info['longitude'] = round(location_info['longitude'],2) #rounding the value upto 2 decimal points

                elev = requests.get(elevation_url + str(location_info['latitude']) + ',' + str(location_info['longitude'])).json()
                if elev.get('results'):
                    for elev_results in elev.get('results'):
                        location_info['elevation'] = elev_results.get('elevation', '')
                        location_info['elevation'] = round(location_info['elevation'],2) #rounding the value upto 2 decimal points
                        break
                else:
                    print("Elevation is returned null!! Please delete past_weather_data.csv file and try again.")
                break

        location_info_list.append(location_info)

    return location_info_list


'''
This function get_weather_data() takes the arguments like
location_info_list - It is a list of dictionary having longitude, latitude and the elevation of different cities.
start_date - It is the date from which we want to record past weather data from.
api_key - To use the forecastio api

It returns the weather_data a dictionary having all the weather data like temperature, humidity, pressure, time, condition
of the city for one year .
'''

def get_weather_data(location_info_list, start_date, api_key):
    weather_data = {}
    for location_info in location_info_list:
        for week in range(0, 365, 7): #Collecting the data after every 7 days throughout the year
            try:
                forecast = forecastio.load_forecast(
                    api_key,
                    location_info['latitude'],
                    location_info['longitude'],
                    time = start_date+datetime.timedelta(week),
                    units = "si"
                    )
                for hour in forecast.hourly().data: #hourly weather data for the next 168 hours ie 7 days
                    weather_data['location'] = weather_data.get('location', []) + [location_info['location']]
                    weather_data['latitude'] = weather_data.get('latitude', []) + [location_info['latitude']]
                    weather_data['longitude'] = weather_data.get('longitude', []) + [location_info['longitude']]
                    weather_data['elevation'] = weather_data.get('elevation', []) + [location_info['elevation']]

                    # To get the condition of the weather - Cloudy, Snow, Clear, Partly Cloudy etc.
                    cond = hour.d.get('summary', '').lower()
                    #print ("----",cond)
                    #For cloudy weather, we will treat it as rain, clear as sunny and snow as snow
                    if 'snow' in cond:
                       weather_data['condition'] = weather_data.get('condition', []) + ['Snow']

                    elif 'clear' in cond:
                        weather_data['condition'] = weather_data.get('condition', []) + ['Sunny']
                        
                    else:
                       weather_data['condition'] = weather_data.get('condition', []) + ['Rain']                        

                    #weather_data['condition'] = weather_data.get('condition', []) + [hour.d.get('summary', '')]
                    weather_data['temperature'] = weather_data.get('temperature', []) + [hour.d.get('temperature')]
                    weather_data['humidity'] = weather_data.get('humidity', []) + [hour.d.get('humidity')]
                    weather_data['pressure'] = weather_data.get('pressure', []) + [hour.d.get('pressure')]
                    weather_data['time'] = weather_data.get('time', []) + [hour.d['time']]
            except Exception as e:
                print("The exception is ",e)
                return weather_data

    return weather_data

if __name__ == '__main__':

    list_of_locations = []
    api_key = '0123456789abcdef9876543210fedcba'  #API key for forecastio
    start_date = datetime.datetime(2016, 1, 1) #The date from which we want to record weather data

    if not os.path.exists('WeatherReport'):
        os.makedirs('WeatherReport')

    try:
        with open('WeatherReport/past_locations.txt') as f:
            for line in f:
                list_of_locations.append(line.strip())
                
    except Exception as e:
        #print(e)
        print("Please create past_locations.txt file in WeatherReport folder and enter cities first.")
        exit()

    # Get the latitude, longitude and elevation for all the locations
    location_info_list = get_location_info(list_of_locations)

    # Generate the weather data in the form of dictionary based on locations for the past one year on an hourly basis
    weather_data = get_weather_data(location_info_list, start_date, api_key)

    # Converting the dictionary into dataframe so that we can write it in the csv file
    df = pandas.DataFrame(weather_data)

    #write the weather data into a file in csv format
    df.to_csv('WeatherReport/past_weather_data.csv')  
