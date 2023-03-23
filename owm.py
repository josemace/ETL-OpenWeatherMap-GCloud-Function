import config
import logging
from datetime import datetime
import pandas as pd
import requests


def collect_weather_data():
    """Collect data from OpenWeatherMap API and save it into a given csv file"""
    
    cities = config.config_vars.get("cities")

    api_key = config.config_vars.get("owm_apikey")

    # Sets the units of measurement
    units = config.config_vars.get("units")
    if units is None:
        units = "standard"

    # Set up lists to store the data
    data = []

    try:
        # Loop through the cities and get the weather data
        for city in cities:
            # Set up API request parameters
            params = {"q": city, "units": units, "appid": api_key}

            # Send API request
            response = r = requests.get("http://api.openweathermap.org/data/2.5/weather", params=params)

            # Get the data from the response
            if response == False:
                return False
            weather_data = response.json()

            # Extract the relevant information and add it to the list
            data.append({
                "Timestamp": datetime.now(),
                "City": city,
                "Temperature": weather_data["main"]["temp"],
                "Minimum Temperature": weather_data["main"]["temp_min"],
                "Maximum Temperature": weather_data["main"]["temp_max"],
                "Humidity": weather_data["main"]["humidity"],
                "Pressure": weather_data["main"]["pressure"],
                "Wind Speed": weather_data["wind"]["speed"]
            })

        # Create a pandas DataFrame from the data
        df = pd.DataFrame(data)
        
        return df
    
    except Exception as e:
        logging.error(f"[Exception] {e} on {e.__traceback__.tb_frame} line {e.__traceback__.tb_lineno}")
