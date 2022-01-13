import urllib.request
import json
import datetime

class weather:

    def __init__(self, lat, lon):
        
        # 받아온 위도, 경도 값을 입력해준다.
        self.__lat = lat
        self.__lon = lon
        
        # url을 열어주고,
        weather_url = 'https://api2.sktelecom.com/weather/current/hourly?version=1&lat={}&lon={}&appKey=8a10f1b6-1962-48ae-9a88-70c3bc5d17c4'.format(self.__lat, self.__lon)
        w_u = urllib.request.urlopen(weather_url)
        # data를 읽어서,
        weather_data = w_u.read()
        # json 형태로 받아온다.
        weather_json = json.loads(weather_data)

        # App_inventor에 보낼 county, name, temperture, humid 값을 url에서 json data형태로 뽑아온다.
        self.__county = weather_json["weather"]["hourly"][0]["grid"]["county"]
        self.__name = weather_json["weather"]["hourly"][0]["sky"]["name"]
        self.__tem = weather_json["weather"]["hourly"][0]["temperature"]["tc"]
        self.__hum = weather_json["weather"]["hourly"][0]["humidity"]

        # pm10_url을 열기위해 필요한 query값인 city를 받아온다.
        self.__sidoName = weather_json["weather"]["hourly"][0]["grid"]["city"].encode("utf-8")

        # url을 열어주고,
        pm10_url = 'geNo=1&numOfRows=10&ServiceKey=Tt1JcvDb%2Fq8Piz5UpSG66v6ny8QRNl9i81FPsLDvW7uiL0hMuUzx1HQG%2BYdCw4ZvI4FAs%2BCm9g3u0Z3GtNnp5Q%3D%3D&ver=1.3'.format(self.__sidoName)
        p_u = urllib.request.urlopen(pm10_url)
        # data를 읽어서,
        pm10_data = p_u.read()
        # json 형태로 받아온다.
        pm10_json = json.loads(pm10_data)
        
        # 현재 미세먼지 등급을 받아온다.
        self.__pm10 = int(pm10_json["list"][0]["pm10Grade"])
    
    # get_method 구현.
    def get_data(self):
        # 데이터들을 list형태로 저장후 리턴해준다.
        self.__dataList = [self.__tem, self.__hum, self.__pm10, self.__name, self.__county]
        return self.__dataList

    def __del__(self):
        return