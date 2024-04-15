from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB Atlas 연결
client = MongoClient('mongodb+srv://jyspress:<password>@cluster0.ninp3j8.mongodb.net/')
db = client['bounce']
collection = db['bounce']

# 모든 뉴스 항목을 가져오는 GET 요청을 처리
@app.route('/news', methods=['GET'])
def get_news():
    news_items = list(collection.find({}, {'_id': 0}))  # MongoDB에서 모든 뉴스 항목을 조회하고, '_id' 필드 제외
    return jsonify(news_items)

# 새로운 뉴스 항목을 추가하는 POST 요청을 처리
@app.route('/news', methods=['POST'])
def add_news():
    news_data = request.get_json()  # 요청 본문에서 JSON 데이터를 파싱
    result = collection.insert_one(news_data)  # MongoDB 컬렉션에 데이터를 추가
    news_data['_id'] = str(result.inserted_id)  # ObjectId를 문자열로 변환하여 JSON 응답에 포함
    return jsonify(news_data), 201  # 추가된 데이터와 함께 201 Created 응답을 반환

if __name__ == '__main__':
    app.run(debug=True, port=3000)  # Flask 앱을 포트 3000에서 실행
