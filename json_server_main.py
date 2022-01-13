from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape
import json
import pickle
import like_method
import weather_API

def application(environ, start_response):

    # query string 사용.
    d = parse_qs(environ['QUERY_STRING'])

    # like 수를 받아온다.
    like_DB = like_method.LikeDB()

    # 사용자의 위도와 경도를 App client로 부터 입력받는다.
    # 그 위치에 따른 data를 받아온다.
    latstr = escape(d.get('latitude', [''])[0])
    lonstr = escape(d.get('longitude', [''])[0])

    # 날씨 API를 class로 지정해준다.
    current_weather_API = weather_API.weather(latstr, lonstr)

    # url path info 지정.
    url_path = environ['PATH_INFO'].split("/")
    
    # 요청한 url == http://localhost:port/like/whatCloth
    # environ['PATH_INFO'] == /like/whatCloth/
    # /like/whatCloth  =>  받아온 url이 'like' 갱신을 요청할 경우.
    # url_path == ['', 'like', 'whatCloth']
    if (url_path[1] == 'like'):
        # url_path[2] 의 옷이 like_dic에 있을경우.
        if (url_path[2] in like_DB.getLikes()):
        
            # url_path[2]  =>  무슨 옷에 'like'를 눌렀는지 받아온다.
            # like_DB.save()  =>  'like' 값을 갱신해준다.
            like_DB.inc(url_path[2])
            like_DB.save()

            status = '200 OK'

            response_body = json.dumps({'status': status, 'code': 'success', 'updated': url_path[2]})
            
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body)))
            ]

            start_response(status, response_headers)

            return [response_body.encode("utf-8")]

        else:

            status = '200 OK'

            response_body = json.dumps({'status': status, 'code': 'failed', 'error': 'cloth is not in dictionary'})
            
            response_headers = [
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body)))
            ]

            start_response(status, response_headers)

            return [response_body.encode("utf-8")]

    
    # 요청한 url == http://localhost:port/getLikes/?location=x&time=y
    # environ['PATH_INFO'] == /getLikes/?location=x&time=y
    # /getLikes/?location=x&time=y  =>  받아온 url이 정보출력을 요청할 경우.
    # url_path == ['', 'getLikes', '?location=x&time=y']
    elif (url_path[1] == "getLikes"):

        # class의 get_method를 이용해 API data를 받아온다.
        current_data = current_weather_API.get_data()

        # response_body 에 들어갈 json_weather, status, like_dic을 지정해준다.
        status = '200 OK'
        
        json_weather = {'temperature': current_data[0], 'humid': current_data[1], 'pm10': current_data[2], 'name': current_data[3]}
        
        like_dic = like_DB.getLikes()
        
        body_data = {}
        body_data.update({'status': status, 'code': 'success'})
        body_data.update(json_weather)
        body_data.update(like_dic)

        # 받아온 data를 response_body에 입력해준다.
        response_body = json.dumps(body_data)
        
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response(status, response_headers)

        return [response_body.encode("utf-8")]
    
    else:
        status = '404 Not Found'

        response_body = json.dumps({'status': status, 'code': 'failed', 'error': 'wrong address!'})

        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response(status, response_headers)
        
        return [response_body.encode("utf-8")]
    
    del like_DB
    del current_weather_API

httpd = make_server('10.30.116.13', 8051, application)
httpd.serve_forever()