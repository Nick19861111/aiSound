# modules/weather_service.py
import requests
import time

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://devapi.qweather.com/v7/weather/now"
        self.location_url = "https://geoapi.qweather.com/v2/city/lookup"

    def get_location_id(self, city):
        params = {
            "key": self.api_key,
            "location": city
        }
        try:
            response = requests.get(self.location_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data["code"] == "200" and data["location"]:
                return data["location"][0]["id"]
            return None
        except requests.RequestException as e:
            print(f"获取城市 ID 失败: {str(e)}")
            return None

    def get_weather(self, city):
        location = self.get_location_id(city)
        if not location:
            return f"{city} 天气：无法获取城市信息"
        params = {
            "key": self.api_key,
            "location": location
        }
        for attempt in range(3):
            try:
                response = requests.get(self.base_url, params=params, timeout=5)
                response.raise_for_status()
                data = response.json()
                if data["code"] != "200":
                    return f"{city} 天气：获取失败，错误代码 {data['code']}"
                weather = data["now"]
                return f"{city} 天气：{weather['text']}，温度 {weather['temp']}°C"
            except requests.RequestException as e:
                print(f"获取天气失败 (尝试 {attempt + 1}/3): {str(e)}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    return f"{city} 天气：获取失败，请检查网络或 API 密钥"