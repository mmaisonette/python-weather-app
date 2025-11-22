"""
Unit tests for the weather module.

This module contains test cases that verify the functionality of the weather module
without making actual API calls. It uses monkeypatching to mock external dependencies
and ensure that weather data retrieval works correctly.

Tests:
    test_get_weather: Verifies that weather.main() correctly integrates the
                      get_lat_lon and get_current_weather functions and returns
                      a properly structured WeatherData object.
"""

import weather
from weather import WeatherData


def test_get_weather(monkeypatch):
    """Ensure weather.main returns WeatherData without hitting real APIs."""

    def fake_get_lat_lon(city_name, country_name, apikey):
        assert city_name == "Toronto"
        assert country_name == "CA"
        return 43.7, -79.4

    def fake_get_current_weather(lat, lon, apikey):
        assert lat == 43.7
        assert lon == -79.4
        return WeatherData(
            main="Clouds",
            description="overcast clouds",
            icon="04d",
            temp=12,
        )

    monkeypatch.setattr(weather, "get_lat_lon", fake_get_lat_lon)
    monkeypatch.setattr(weather, "get_current_weather", fake_get_current_weather)

    result = weather.main("Toronto", "CA")

    assert isinstance(result, WeatherData)
    assert result.main == "Clouds"
    assert result.description == "overcast clouds"
    assert result.icon == "04d"
    assert result.temp == 12
