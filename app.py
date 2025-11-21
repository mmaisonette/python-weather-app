"""
Flask web application for displaying weather information.

This module creates a simple web application that allows users to input a city
and country name to retrieve weather information. It uses Flask for the web
framework and integrates with a weather module to fetch weather data.

Routes:
    / (GET, POST): Main route that handles both displaying the form and
                   processing weather requests.

Attributes:
    app (Flask): The Flask application instance.
"""

from flask import Flask, render_template, request
from weather import main as get_weather

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the index route for the weather application.

    This function processes both GET and POST requests. On POST requests, it retrieves
    the city and country names from the form data, fetches weather information using
    the get_weather function, and passes the data to the template for rendering.

    Returns:
        str: Rendered HTML template with weather data if available, or None if GET request.

    Form Parameters:
        cityName (str): The name of the city to fetch weather data for.
        countryName (str): The name of the country where the city is located.
    """

    data = None
    if request.method == 'POST':
        city = request.form['cityName']
        country = request.form['countryName']
        data = get_weather(city, country)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
