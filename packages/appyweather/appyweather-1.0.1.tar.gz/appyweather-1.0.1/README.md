## Description

Appyweather is a Python package that provide you with 24-hour weather forecast information for any city 
or location (lat/lon), and it is mainly created for educational reasons. 
All weather data are provided through the 'openweathermap' api service.

- Get your own api-key from: https://openweathermap.org
- Api-key might take a few hours to be activated.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install appyweather.

```bash
pip install appyweather
```

## Usage

```python
from appyweather import Weather

# using a city name
weather = Weather(api_key='yourapikeyhere', city='Athens')

# using latitude/longitude coordinates + units (optional)
weather = Weather(api_key='yourapikeyhere', lat=37.98, lon=23.72, units='metric')

# get all the weather data for the next 24 hours (json)
weather.next_24_hours()

# Get basic weather data (datetime, temperature, sky condition, sky condition icon code) for the next 24 hours.
weather.next_24_hours_basic()
```

- Sample url for sky condition icons: http://openweathermap.org/img/wn/10d@2x.png

## License
[MIT](https://choosealicense.com/licenses/mit/)