from flask import Flask, Response
import json

def get_data():
    data = {
        'stations': ['강남역', '역삼역', '서울역'],
        'ridership': [1000, 800, 1200]
    }
    response = Response(
        json.dumps(data, ensure_ascii=False),  # ensure_ascii=False를 설정하여 JSON에 유니코드 문자 포함
        mimetype='application/json; charset=utf-8'  # charset=utf-8을 명시적으로 설정
    )
    return response