from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
import email_downloader  # 이메일 처리 모듈 임포트
from bson import ObjectId, json_util
from bson.errors import InvalidId


app = Flask(__name__)
CORS(app)

# MongoDB Atlas 연결
client = MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
db = client['bounce']
news_collection = db['news']  # 뉴스 컬렉션
emails_collection = db['emails']  # 이메일 컬렉션

def fetch_emails_from_db():
    try:
        # 첨부파일 정보를 포함하여 이메일을 조회
        emails = list(emails_collection.find({}, {'attachments': 1, 'subject': 1, 'date': 1, 'from': 1}))
        return json_util.dumps(emails)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    

@app.route('/')
def home():
    return "Welcome to the News API", 200

# 모든 뉴스 항목을 가져오는 GET 요청을 처리
@app.route('/news', methods=['GET'])
def get_news():
    news_items = list(news_collection.find({}, {'_id': 0}))  # MongoDB에서 모든 뉴스 항목을 조회하고, '_id' 필드 제외
    return jsonify(news_items)

# 새로운 뉴스 항목을 추가하는 POST 요청을 처리
@app.route('/news', methods=['POST'])
def add_news():
    news_data = request.get_json()  # 요청 본문에서 JSON 데이터를 파싱
    result = news_collection.insert_one(news_data)  # MongoDB 컬렉션에 데이터를 추가
    news_data['_id'] = str(result.inserted_id)  # ObjectId를 문자열로 변환하여 JSON 응답에 포함
    return jsonify(news_data), 201  # 추가된 데이터와 함께 201 Created 응답을 반환

@app.route('/fetch-emails')
def fetch_emails():
    try:
        email_address = 'jys@pedien.com'  # 이메일 주소
        password = '8IVI5wQNZ2hW'  # 이메일 비밀번호
        save_path = '/path_to_save_attachments'  # 첨부 파일을 저장할 경로
        email_downloader.download_attachments('jys@pedien.com', '8IVI5wQNZ2hW', '/path_to_save_attachments')
        return jsonify({'status': 'success', 'message': 'Emails fetched and attachments downloaded'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    
    
    
@app.route('/api/emails', methods=['GET'])
def get_emails():
    emails_json = fetch_emails_from_db()  # DB에서 이메일 데이터를 가져오는 함수
    print(emails_json)  # 서버 로그에 출력
    return Response(emails_json, mimetype='application/json')  # JSON 문자열을 직접 반환



@app.route('/api/emails/<id>', methods=['GET'])
def get_email_detail(id):
    try:
        # ObjectId 생성 시 유효하지 않은 id 값에 대한 예외 처리
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': 'Invalid ID format'}), 400

    try:
        email = emails_collection.find_one({'_id': object_id})
        if email:
            return Response(json_util.dumps(email), mimetype='application/json')
        else:
            return jsonify({'error': 'Email not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)  
