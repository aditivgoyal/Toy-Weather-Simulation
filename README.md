# Toy-Weather-Simulation
To design a weather simulation data for various locations on Earth

# Task

Create a toy simulation of the environment (taking into account things like atmosphere, topography, geography, oceanography, or similar) that evolves over time. Then take measurements at various locations and times, and have your program emit that data, as in the following:

Sydney|-33.86,151.21,39|2015-12-23T05:02:12Z|Rain|+12.5|1004.3|97

Melbourne|-37.83,144.98,7|2015-12-24T15:30:55Z|Snow|-5.3|998.4|55

Adelaide|-34.92,138.62,48|2016-01-03T12:35:37Z|Sunny|+39.4|1114.1|12

where,

• Location is an optional label describing one or more positions,

• Position is a comma-separated triple containing latitude, longitude, and elevation in metres above sea
level,

• Local time is an ISO8601 date time,

• Conditions is either Snow, Rain, Sunny,

• Temperature is in °C,

• Pressure is in hPa, and

• Relative humidity is a %.


# Solution
In order to predict the weather, we can either use direct apis like weather and geopy etc. to determine the forecast for the next 14 days or so.
But, we can also use a Machine Learning approach. In this approach, we record the hourly weather data of 10 different cities for a year.
And based on this previous recorded data, we will predict the weather of new different cities at a new different time.

For this, we will use Linear Regression model where we will provide the location (Latitude, Longitude and Elevation) of the city as input x and y as the other parameters such as temperature or humidity or pressure.

# Prerequisites
In order to run this program successfully, we need to first install few apis by using the following commands on the command prompt:

pip install pandas

pip install scipy

pip install python-forecastio

After this, create a new txt file as past_locations.txt under WeatherReport folder. Enter 10 different cities from all parts of the world.

Next, run RecordWeather.py file to record the weather data for 10 different cities. To run this file type python RecordWeather.py in the command prompt. 

Wait for few minutes as it takes time to record all the data. The weather data generated is recorded in file named as past_weather_data.csv under WeatherReport folder.

Now, create another text file as new_locations.txt under WeatherReport folder. Enter the name of the cities for which you want to predict weather.

Run GenerateWeather.py file by typing python GenerateWeather.py on the command prompt.
This program will write the predicted data in new_weather_data.csv file.


