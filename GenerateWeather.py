
import datetime
import os
import pandas
from sklearn import linear_model
import random
from sklearn.naive_bayes import GaussianNB

import RecordWeather

'''
The function get_linear_humidity() is designed to return a linear regression model
based on following arguments:
input_x - Latitude, Longitude, Elevation and Time
input_y - Humidity

'''

def get_linear_humidity(df):

    humidity_linear_model = linear_model.LinearRegression()
    input_x = df[['latitude', 'longitude', 'elevation', 'time']].values
    input_y = df[['humidity']].values
    
    humidity_linear_model.fit(input_x, input_y)

    return humidity_linear_model

'''
The function get_linear_temperature() is designed to return a linear regression model
based on following arguments:
input_x - Latitude, Longitude, Elevation and Time
input_y - Temperature

'''
def get_linear_temperature(df):

    temperature_linear_model = linear_model.LinearRegression()
    input_x = df[['latitude', 'longitude', 'elevation', 'time']].values
    input_y = df[['temperature']].values
    
    temperature_linear_model.fit(input_x, input_y)

    return temperature_linear_model

'''
The function get_linear_pressure() is designed to return a linear regression model
based on following arguments:
input_x - Latitude, Longitude, Elevation and Time
input_y - Pressure

'''
def get_linear_pressure(df):

    pressure_linear_model = linear_model.LinearRegression()
    input_x = df[['latitude', 'longitude', 'elevation', 'time']].values
    input_y = df[['pressure']].values
    
    pressure_linear_model.fit(input_x, input_y)
    
    return pressure_linear_model

'''
The function get_gaussian_condition() is designed to return a Gaussian model
based on following arguments:
input_x - Latitude, Longitude, Elevation and Time
input_y - Condition
Since the input_y is a string value, we use Gaussian model instead of linear regression model.

'''
def get_gaussian_condition(df):
    condition_gaussian_model = GaussianNB()
    input_x = df[['latitude', 'longitude', 'elevation', 'time']].values
    input_y = df[['condition']].values
    condition_gaussian_model.fit(input_x, input_y)
    return condition_gaussian_model



'''
The function predict_weather_data() is supposed to return the weather data based on all the linear and Gaussian models
We will predict the data based on the random generated time.
This data is returned in a dictionary format.
'''
def predict_weather_data(location_info_list, humidity_model, temperature_model, pressure_model, condition_model, start_date):

    predicted_weather_data = {}

    delta = datetime.timedelta(365)  
    seconds = delta.days*24*60*60 + delta.seconds #number of seconds in 365 days
    
    for location_info in location_info_list:
        location = location_info['location']
        latitude = location_info['latitude']
        longitude = location_info['longitude']
        elevation = location_info['elevation']
        
 
        random_seconds = random.randrange(seconds) #random number of seconds within 365 days from the start_date
        new_date = start_date + datetime.timedelta(seconds = random_seconds)
        
        
        time = int((new_date).strftime('%s'))

        predicted_weather_data['Location'] = predicted_weather_data.get('Location', []) + [location]
        predicted_weather_data['Position'] = predicted_weather_data.get('Position', []) + [str(latitude) + ',' + str(longitude) + ',' + str(elevation)]
        predicted_weather_data['Local Time'] = predicted_weather_data.get('Local Time', []) + [new_date.isoformat()]

        temperature = round(temperature_model.predict([[latitude, longitude, elevation, time]])[0][0],2)          
        predicted_weather_data['Temperature'] = predicted_weather_data.get('Temperature', []) + [temperature]

        pressure = round(pressure_model.predict([[latitude, longitude, elevation, time]])[0][0],2)
        predicted_weather_data['Pressure'] = predicted_weather_data.get('Pressure', []) + [pressure]

        humidity = humidity_model.predict([[latitude, longitude, elevation, time]])[0][0]
        predicted_weather_data['Humidity'] = predicted_weather_data.get('Humidity', []) + [int(humidity * 100)]


        condition = condition_model.predict([[latitude, longitude, elevation, time]])[0]
        predicted_weather_data['Conditions'] = predicted_weather_data.get('Conditions', []) + [condition]
 
    return predicted_weather_data

if __name__ == '__main__':
    '''
    To predict weather for different cities, we will use the linear regression model
    Gaussian naive bayes model is used to predict the value of the condition which is a string.
    '''
    #Read the data from our previously recorded weather of cities for past one year
    df = pandas.read_csv('WeatherReport/past_weather_data.csv')
    #Fill NA values with the mean of the values of that column
    df = df.fillna(df.mean()) 
    
    
    humidity_model = get_linear_humidity(df)    
    pressure_model = get_linear_pressure(df)
    temperature_model = get_linear_temperature(df)
    condition_model = get_gaussian_condition(df)

    # Date from which we will start generating data randomly
    start_date = datetime.datetime(2017, 1, 1)

    # list of locations for which we are generating data
    list_of_locations = []

    try:
        with open('WeatherReport/new_locations.txt') as f:
            for line in f:
                list_of_locations.append(line.strip())
    except Exception as e:
        print("Please create a new_locations.txt file in WeatherReport folder and enter the cities first.")
        exit()
        
    # Get the latitude, longitude and elevation for all the locations
    location_info_list = RecordWeather.get_location_info(list_of_locations)
    
    # Get the predicted weather data in the form of dictionary based on locations
    predicted_weather_data = predict_weather_data(location_info_list, humidity_model, temperature_model, pressure_model, condition_model, start_date)

    # Converting the dictionary into dataframe so that we can write it in the csv file
    df = pandas.DataFrame(predicted_weather_data)

    #Writing to the csv file
    df.to_csv(
        "WeatherReport/new_weather_data.csv",
        columns = ["Location", "Position", "Local Time", "Conditions", "Temperature", "Pressure", "Humidity"],
        header=0,
        index=0,
        sep='|'
    )
