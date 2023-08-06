import requests


class Weather:
    """
    Creates a Weather object by getting the following as input: api-key, city name or latitude/longitude coordinates,
    temperature units (optional). If no units (metric/imperial) are supplied, kelvin units are applied as the default
    units convention.

    Example of package usage:

    # Get your own api-key from: https://openweathermap.org\n
    # Api-key might take a few hours to be activated.\n
    # Using a city name:\n
    >> weather = Weather(api_key='yourapikeyhere', city='Athens')\n
    # Using latitude/longitude coordinates + units (optional):\n
    >> weather = Weather(api_key='yourapikeyhere', lat=37.98, lon=23.72, units='metric')\n
    # Get all the weather data for the next 24 hours (json):\n
    >> weather.next_24_hours()\n
    # Get basic weather data (date, time, temperature, sky condition, sky condition icon code) for the next 24 hours.\n
    >> weather.next_24_hours_basic()\n
    # Sample url for sky condition icons: http://openweathermap.org/img/wn/10d@2x.png
    """

    def __init__(self, api_key, city=None, lat=None, lon=None, units=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
            response = requests.get(url=url)
            self.data = response.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units={units}"
            response = requests.get(url=url)
            self.data = response.json()
        else:
            raise TypeError('provide either a city name or latitude and longitude arguments.')

        if self.data['cod'] != '200':
            raise ValueError(self.data['message'])

    def next_24_hours(self):
        """
        Returns 3-hour weather data for the next 24 hours as a dict.
        """
        all_data = self.data['list'][:9]
        return all_data

    def next_24_hours_basic(self):
        """
        Returns 3-hour basic weather data (date, time, temperature, sky condition, sky condition icon code)
        for the next 24 hours as a list of tuples.
        """
        basic_data = []
        for item in self.data['list'][:9]:
            basic_data.append(
                (item['dt_txt'], item['main']['temp'], item['weather'][0]['description'].title(),
                 item['weather'][0]['icon'])
            )

        return basic_data

