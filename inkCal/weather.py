import logging
import requests
import time

class Weather():    


    def __init__(self, city, api_key):
        self.lon = None
        self.lat = None
        self.city = city
        self.api_key = api_key

        self.weather_data = None
        self.weather_data_time = None

        self.log = logging.getLogger("weather")


    def getString(self):
        w = self.get_weather_data()

        if w is None or "main" not in w or "weather" not in w or len(w["weather"]) < 1:
            return None

        temper = w["main"]["temp"]

        weather_main = w["weather"][0]["main"]
        return f"{weather_main} {temper:.1f}C"

    def getIcon(self):
        w = self.get_weather_data()

        if w is None or "main" not in w or "weather" not in w or len(w["weather"]) < 1:
            return None

        icon_code =  w["weather"][0]["icon"]

        if icon_code.startswith("01"):
            return "icon-sun.png"
        if icon_code.startswith("02"):
            return "icon-cloud.png"
        if icon_code.startswith("03") or icon_code.startswith("04"):
            return "icon-cloud.png"
        if icon_code.startswith("09") or icon_code.startswith("10") or icon_code.startswith("11"):
            return "icon-rain.png"
        if icon_code.startswith("13"):
            return "icon-snow.png"
        if icon_code.startswith("50"):
            # mist
            return "icon-cloud.png"
        return ""

    def get_weather_data(self):
        # Weather data exists

        # TODO: Check that data is not to old
        if self.weather_data and self.weather_data_time:
            # Chack age. Max 3 hours
            now = time.time()

            if self.weather_data_time + 3*60*60 > now:
                return self.weather_data

        if self.city is None or self.api_key is None:
            return None

        # First time; Get city lat/lon
        if self.lon is None:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={self.api_key}"
            response = requests.get(geo_url)
            if response.status_code > 299:
                self.log.error(f"Failed to get geo data for {self.city}: Error: ", {response.text})
                return None

            jsonres = response.json()
            if jsonres is None or len(jsonres) != 1:
                self.log.error(f"City not found/not unique {self.city}")
                return None

            self.lat = jsonres[0]["lat"]
            self.lon = jsonres[0]["lon"]

        if self.lat is None or self.lon is None:
            self.log.error(f"Cannot fetch weather, unknown lat/lon")
            return None


        # Get heather. Look for first weather with time 15:00

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.lat}&lon={self.lon}&units=metric&appid={self.api_key}"

        response = requests.get(url)
        if response.status_code >299:
            self.log.error(f"Failed to get weather: Error: ", {response.text})
            return None

        weather_json = response.json()
        if weather_json is None or "list" not in weather_json:
            self.log.error(f"No list with weather in response")
            return None

        weather_list = weather_json["list"]
        for weather in weather_list:
            if "dt_txt" in weather and "15:00:00" in weather["dt_txt"]:
                self.weather_data = weather
                self.weather_data_time = time.time()
                return weather
