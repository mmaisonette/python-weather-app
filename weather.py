"""
Weather Application Module

This module provides functionality to fetch weather data for a specified city and country
using the OpenWeatherMap API. It retrieves geographical coordinates and current weather
information, returning structured weather data.

The module uses environment variables to securely store the API key and implements
dataclasses for clean data representation.

Functions:
    - get_lat_lon(city_name, country_name, apikey): Retrieves latitude and longitude coordinates
    for a given city and country.
    - get_current_weather(lat, lon, apikey): Fetches current weather data for specified coordinates.
    - main(city_name, country_name): Orchestrates the weather data retrieval process.

Classes:
    - WeatherData: A dataclass that stores weather information including main condition,
    description, icon code, and temperature.

Requirements:
    - os: For grabbing the environment variable at runtime.
    - dataclasses: For combine weather information into a dataclass.
    - requests: For making HTTP requests to the OpenWeatherMap API.
    - python-dotenv: For loading environment variables from .env file.
    - API_KEY: OpenWeatherMap API key stored in environment variables.
    It is stored in the .env file.

Example:
    weather = main("London", "UK")
    print(f"{weather.description}, {weather.temp}°C")
"""

import os
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


@dataclass
class WeatherData:
    """
    A data class representing weather information.

    Attributes:
        - main (str): The main weather condition category (e.g., 'Clear', 'Rain', 'Clouds').
        - description (str): A detailed description of the weather condition.
        - icon (str): The weather icon identifier or code.
        - temp (int): The temperature value (represented in Celsius).
    """

    main: str
    description: str
    icon: str
    temp: int


def get_lat_lon(city_name, country_name, apikey):
    """
    Retrieve the latitude and longitude coordinates for a specified city and country.

    This function makes a request to the OpenWeatherMap API to fetch geographical
    coordinates (latitude and longitude) for the given city and country combination.

    Args:
        - city_name (str): The name of the city to look up.
        - country_name (str): The name or code of the country where the city is located.
        - apikey (str): The API key for authenticating with the OpenWeatherMap API.

    Returns:
        - tuple: A tuple containing two elements (lat, lon) where:
            - lat (float or None): The latitude of the city, or None if not found.
            - lon (float or None): The longitude of the city, or None if not found.

    Example:
        lat, lon = get_lat_lon('London', 'UK', 'your_api_key')
        print(f"Coordinates: {lat}, {lon}")
    """

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{country_name}&appid={apikey}",
        timeout=10,
    ).json()
    coord = response.get("coord", {})
    lat, lon = coord.get("lat"), coord.get("lon")
    return lat, lon


def get_current_weather(lat, lon, apikey):
    """
    Retrieves current weather data for a specific location from OpenWeatherMap API.

    Args:
        - lat (float): Latitude coordinate of the location.
        - lon (float): Longitude coordinate of the location.
        - apikey (str): OpenWeatherMap API key for authentication.

    Returns:
        - WeatherData: An object containing weather information with the following attributes:
            - main (str): Main weather condition (e.g., 'Rain', 'Clear').
            - description (str): Detailed weather description.
            - icon (str): Weather icon code.
            - temp (int): Current temperature in Celsius (rounded to nearest integer).

    Raises:
        - requests.exceptions.RequestException: If the API request fails.
        - KeyError: If the expected data fields are not present in the API response.
    """

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric",
        timeout=10,
    ).json()
    data = WeatherData(
        main=response.get("weather")[0].get("main"),
        description=response.get("weather")[0].get("description"),
        icon=response.get("weather")[0].get("icon"),
        temp=int(response.get("main").get("temp")),
    )
    return data


def main(city_name, country_name):
    """
    Retrieve current weather data for a specified city and country.

    This function takes a city name and country name as input, retrieves the
    geographical coordinates (latitude and longitude) for that location, and
    then fetches the current weather data for those coordinates.

    Args:
        - city_name (str): The name of the city for which to retrieve weather data.
        - country_name (str): The name of the country where the city is located.

    Returns:
        - dict: A dictionary containing current weather data for the specified location.
              - The exact structure depends on the API response from get_current_weather().

    Raises:
        - May raise exceptions from get_lat_lon() or get_current_weather() if the API
        calls fail or if the location cannot be found.

    Note:
        This function requires 'api_key' to be defined in the current scope.
    """

    lat, lon = get_lat_lon(city_name, country_name, api_key)
    weather_data = get_current_weather(lat, lon, api_key)
    return weather_data
