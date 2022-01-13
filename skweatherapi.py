#-*- coding:utf-8 -*-
import sys
import requests

# SK Planet에서 키 요청 받아야 함.
# https://developers.sktelecom.com
# 앱 등록 및 키 발급
appKey = "8a10f1b6-1962-48ae-9a88-70c3bc5d17c4"

url_weather = 'https://api2.sktelecom.com/weather/'
# 현재 날씨(시간별)
url_hourly = url_weather+'current/hourly'
# 현재 날씨(분별)
url_minutely = url_weather+'current/minutely'
# 간편 날씨 (어제, 오늘, 내일, 모레)
url_summary = url_weather+'summary'

headers = {'Content-Type': 'application/json; charset=utf-8',
           'appKey': appKey}

HOURLY = 0
MINUTELY = 1

YESTERDAY = -1
TODAY     = 0
TOMORROW  = 1
DAYAFTERTOMORROW = 2

def changeSkyName(txt):
    dic = {
            #과거
            'Y':
            {'01': '맑았',
            '02': '구름조금 있었',
            '03': '구름이 많았',
            '04': '구름이 많았고 비 내렸',
            '05': '구름이 많았고 눈 내렸',
            '06': '구름이 많았고 비 또는 눈 내렸',
            '07': '흐렸',
            '08': '흐리고 비가 내렸',
            '09': '흐리고 눈이 내렸',
            '10': '흐리고 비 또는 눈 내렸',
            '11': '흐리고 낙뢰 있었',
            '12': '뇌우와 비이 내렸',
            '13': '뇌우와 눈이 내렸',
            '14': '뇌우와 비 또는 눈이 내렸'},
           #현재
           'A':
           {'01': '맑',
            '02': '구름이 조금 있',
            '03': '구름이 많',
            '04': '구름이 많고 비가 내리',
            '05': '구름이 많고 눈 내리',
            '06': '구름이 많고 비 또는 눈 내리',
            '07': '흐리',
            '08': '흐리고 비가 내리',
            '09': '흐리고 눈이 내리',
            '10': '흐리고 비 또는 눈이 내리',
            '11': '흐리고 낙뢰가 있',
            '12': '뇌우와 비가 내리',
            '13': '뇌우와 눈이 내리',
            '14': '뇌우와 비 또는 눈이 내리'},
            #예측
            'M':
            {'01': '맑을 것',
             '02': '구름이 조금 있을 것',
             '03': '구름이 많을 것',
             '04': '구름이 많고 비가 내릴 것',
             '05': '구름이 많고 눈이 내릴 것',
             '06': '구름이 많고 비 또는 눈이 내릴 것',
             '07': '흐릴 것',
             '08': '흐리고 비가 내릴 것',
             '09': '흐리고 눈이 내릴 것',
             '10': '흐리고 비 또는 눈이 내릴 것',
             '11': '흐리고 낙뢰가 있을 것',
             '12': '뇌우와 비가 내릴 것',
             '13': '뇌우와 눈이 내릴 것',
             '14': '뇌우와 비 또는 눈이 내릴 것'}}
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    #ex SKY_A13
    #code = A13
    code = txt.split('_')[1]
    #mode = A
    mode = code[0:1]
    #num = 13
    num = code[1:]
    #print(mode)
    #print(num)
    if mode == 'Y':
        ret = dic['Y'][num]
    elif mode == 'M':
        ret = dic['M'][num]
    else:
        ret = dic['A'][num]
    return ret

#간변 날씨(시간별)
def summary(weather, reqDay):
    # print(weather)

    # 발표 시간
    timeRelease  = weather['timeRelease']

    # 격자정보
    # 위도
    grid_latitude  = weather['grid']['latitude']
    # 경도
    grid_longitude = weather['grid']['longitude']
    # 시, 도
    grid_city      = weather['grid']['city']
    # 시, 군, 구
    grid_county    = weather['grid']['county']
    # 읍, 면, 동
    grid_village   = weather['grid']['village']

    yesterday      = weather['yesterday']
    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈

    yesterday_sky_name      = yesterday['sky']['name']
    yesterday_sky_code      = yesterday['sky']['code']
    yesterday_temperature_tmax = yesterday['temperature']['tmax'] #최고기온
    yesterday_temperature_tmin = yesterday['temperature']['tmin'] #최저기온
    yesterday_precipitation_rain = yesterday['precipitation']['rain']
    yesterday_precipitation_snow = yesterday['precipitation']['snow']
    changeSkyName(yesterday_sky_code)

    today      = weather['today']
    today_sky_name      = today['sky']['name']
    today_sky_code      = today['sky']['code']
    today_temperature_tmax = today['temperature']['tmax'] #최고기온
    today_temperature_tmin = today['temperature']['tmin'] #최저기온

    tomorrow      = weather['tomorrow']
    tomorrow_sky_name      = tomorrow['sky']['name']
    tomorrow_sky_code      = tomorrow['sky']['code']
    tomorrow_temperature_tmax = tomorrow['temperature']['tmax'] #최고기온
    tomorrow_temperature_tmin = tomorrow['temperature']['tmin'] #최저기온

    dayAfterTomorrow      = weather['dayAfterTomorrow']
    dayAfterTomorrow_sky_name      = dayAfterTomorrow['sky']['name']
    dayAfterTomorrow_sky_code      = dayAfterTomorrow['sky']['code']
    dayAfterTomorrow_temperature_tmax = dayAfterTomorrow['temperature']['tmax'] #최고기온
    dayAfterTomorrow_temperature_tmin = dayAfterTomorrow['temperature']['tmin'] #최저기온


    if reqDay == YESTERDAY:
        sky_name = '어제 하늘은 ' + changeSkyName(yesterday_sky_code) + '습니다.'
        temperature_max = yesterday_temperature_tmax
        temperature_min = yesterday_temperature_tmin
        endofText = '였습니다.'
    elif reqDay == TODAY:
        sky_name = '오늘 하늘은 ' + changeSkyName(today_sky_code) + '습니다.'
        temperature_max = today_temperature_tmax
        temperature_min = today_temperature_tmin
        endofText = '입니다.'
    elif reqDay == TOMORROW:
        sky_name = '내일 하늘은 ' + changeSkyName(tomorrow_sky_code) + '으로 예상됩니다.'
        temperature_max = tomorrow_temperature_tmax
        temperature_min = tomorrow_temperature_tmin
        endofText = '일 것으로 예상됩니다.'
    elif reqDay == DAYAFTERTOMORROW:
        sky_name = '모레 하늘은 ' + changeSkyName(dayAfterTomorrow_sky_code) + '으로 예상됩니다.'
        temperature_max = dayAfterTomorrow_temperature_tmax
        temperature_min = dayAfterTomorrow_temperature_tmin
        endofText = '일 것으로 예상됩니다.'
    else:
        sky_name = '내일 하늘은 ' + changeSkyName(tomorrow_sky_code) + '으로 예상됩니다.'
        temperature_max = tomorrow_temperature_tmax
        temperature_min = tomorrow_temperature_tmin
        endofText = '일 것으로 예상됩니다.'

    #현재 기온 + 날씨 + 풍속
    fTemper = float(temperature_max)
    temp = ''
    #영하 표시
    if fTemper < 0:
        temp = '영하 '
        fTemper = abs(fTemper)
    tempMax = temp + str(fTemper)

    #현재 기온 + 날씨 + 풍속
    fTemper = float(temperature_min)
    temp = ''
    #영하 표시
    if fTemper < 0:
        temp = '영하 '
        fTemper = abs(fTemper)

    tempMin = temp + str(fTemper)

    txt = ''
    txt = sky_name + ' 최고 기온은 '
    txt = txt + tempMax + ' 도 최저 기온은 '
    txt = txt + tempMin + ' 도 ' + endofText
    return txt

#현재 날씨(시간별)
def hourly(weather):
    # 상대 습도
    humidity     = weather['humidity']

    # 발표 시간
    timeRelease  = weather['timeRelease']

    # 격자정보
    # 위도
    grid_latitude  = weather['grid']['latitude']
    # 경도
    grid_longitude = weather['grid']['longitude']
    # 시, 도
    grid_city      = weather['grid']['city']
    # 시, 군, 구
    grid_county    = weather['grid']['county']
    # 읍, 면, 동
    grid_village   = weather['grid']['village']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']

    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    #현재 기온 + 날씨 + 풍속
    fTemper = float(temperature_tc)
    temp = ''
    #영하 표시
    if fTemper < 0:
        temp = '영하 '
        fTemper = abs(fTemper)


    temp = temp + str(fTemper)

    txt = '현재 하늘은 ' + sky_name + '이고, 기온은 ' + temp + ' 도 입니다.'

    #print(txt)
    return txt


#현재 날씨(분별)
def minutely(weather):
    #print(weather)

    # 상대 습도
    humidity     = weather['humidity']
    # 기압정보
    # 현지기압(Ps)
    pressure_surface  = weather['pressure']['surface']
    # 해면기압(SLP)
    pressure_seaLevel  = weather['pressure']['seaLevel']
    # 관측소
    # 관측소명
    station_name      = weather['station']['name']
    # 관측소 지점번호(stnid)
    station_id      = weather['station']['id']
    # 관측소 유형
    #- KMA: 기상청 관측소
    #- BTN: SKP 관측소
    station_type  = weather['station']['type']
    # 위도
    station_latitude  = weather['station']['latitude']
    # 경도
    station_longitude = weather['station']['longitude']

    # 기온 정보
    # 오늘의 최고기온
    temperature_tmax = weather['temperature']['tmax']
    # 1시간 현재기온
    temperature_tc = weather['temperature']['tc']
    # 오늘의 최저기온
    temperature_tmin = weather['temperature']['tmin']

    # 낙뢰유무(해당 격자 내)
    # - 0: 없음
    # - 1: 있음
    lightning = weather['lightning']

    # 강수량
    # 강수형태코드
    # - 0: 현상없음 → rain(sinceOntime) 사용
    # - 1: 비       → rain(sinceOntime) 사용
    # - 2: 비/눈 → precipitation(sinceOntime) 사용
    # - 3: 눈    → precipitation(sinceOntime) 사용
    precipitation_type = weather['precipitation']['type']
    # 1시간 누적 강수량
    # - if type=0/1/2 → 강우량 (mm)
    # - if type=3     → 적설량 (cm)
    precipitation_sinceOntime = weather['precipitation']['sinceOntime']

    # 바람정보
    # 풍향 (dgree)
    wind_wdir = weather['wind']['wdir']
    # 풍속 (m/s)
    wind_wspd = weather['wind']['wspd']

    # 하늘 상태 정보
    # 하늘상태코드명
    # - SKY_A01: 맑음
    # - SKY_A02: 구름조금
    # - SKY_A03: 구름많음
    # - SKY_A04: 구름많고 비
    # - SKY_A05: 구름많고 눈
    # - SKY_A06: 구름많고 비 또는 눈
    # - SKY_A07: 흐림
    # - SKY_A08: 흐리고 비
    # - SKY_A09: 흐리고 눈
    # - SKY_A10:  흐리고 비 또는 눈
    # - SKY_A11: 흐리고 낙뢰
    # - SKY_A12: 뇌우, 비
    # - SKY_A13: 뇌우, 눈
    # - SKY_A14: 뇌우, 비 또는 눈
    sky_name = weather['sky']['name']
    # 하늘상태코드
    sky_code = weather['sky']['code']

    # 강우정보
    # 1시간 누적 강우량
    rain_sinceOntime   = weather['rain']['sinceOntime']
    # 일 누적 강우량
    rain_sinceMidnight = weather['rain']['sinceMidnight']
    # 10분 이동누적 강우량
    rain_last10min     = weather['rain']['last10min']
    # 15분 이동누적 강우량
    rain_last15min     = weather['rain']['last15min']
    # 30분 이동누적 강우량
    rain_last30min     = weather['rain']['last30min']
    # 1시간 이동누적 강우량
    rain_last1hour     = weather['rain']['last1hour']
    # 6시간 이동누적 강우량
    rain_last6hour     = weather['rain']['last6hour']
    # 12시간 이동누적 강우량
    rain_last12hour    = weather['rain']['last12hour']
    # 24시간 이동누적 강우량
    rain_last24hour    = weather['rain']['last24hour']


    #현재 기온 + 날씨 + 풍속
    fTemper = float(temperature_tc)
    temp = ''
    #영하 표시
    if fTemper < 0:
        temp = '영하 '
        fTemper = abs(fTemper)

    temp = temp + str(fTemper)
    #현재 기온 + 날씨 + 풍속

    txt = '현재 하늘은 ' + sky_name + '이고, 기온은 ' + temp + ' 도 입니다.'

    return txt

def requestSummaryWeather(lat='37.5714000000', lon ='126.96580000000', stnid = '108', subData = TODAY):
    params_summary = { "version": "1",
                "lat": lat,
                "lon": lon,
                "stnid": stnid }

    response = requests.get(url_summary, params=params_summary, headers=headers)

    ret2 = ''

    if response.status_code == 200:
        response_body = response.json()
        weather_data = response_body['weather']['summary'][0]
        ret = summary(weather_data, subData)
        return ret
    else:
        pass
        print(response.status_code)
        return response.status_code
        #에러
    return ret

def requestCurrentWeather(city = '경기', county = '김포시', village = '장기동', requestMode = HOURLY):
    params = { "version": "1",
                "city": city,
                "county": county,
                "village": village }

    # 시간별
    if requestMode == HOURLY:
        response = requests.get(url_hourly, params=params, headers=headers)
    else: #분별
        response = requests.get(url_minutely, params=params, headers=headers)

    ret2 = ''

    if response.status_code == 200:
        response_body = response.json()
        if requestMode == HOURLY:
            weather_data = response_body['weather']['hourly'][0]
            ret = hourly(weather_data)
        else:
            weather_data = response_body['weather']['minutely'][0]
            ret = minutely(weather_data)
        return ret
    else:
        pass
        print(response.status_code)
        return response.status_code
        #에러

    return ret

if __name__ == '__main__':
    #city = '경기'  #'도' 나 '시'는 빼고 넣는다.
    #county = '김포시' #시 or 구
    #village = '장기동' #동
    # 시간별 (기본)
    print('간단하게')
    txt = requestSummaryWeather(subData = TODAY)
    print(txt)

    print('분별')
    txt = requestCurrentWeather('경기','김포시','장기동', MINUTELY)
    print(txt)

    print('시간별')
    txt = requestCurrentWeather('경기','김포시','장기동', HOURLY)
    print(txt)
