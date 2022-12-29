import json

class Settings:

    default_settings_file = "inkCal.json"

    ROTATION = "rotation"
    CITY = "city"
    API_KEY = "api_key"

    def __init__(self, file_name = default_settings_file, json_data = None):
        if (json_data):
            self.settings_json = json_data
            return

        try:
            with open(file_name) as f:
                self.settings_json = json.load(f)
        except:
            print ("Cannot open json")

    def get(self, key):
        if key in self.settings_json:
            return self.settings_json[key]
        