from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from pymongo import MongoClient
import email_downloader  # 이메일 처리 모듈 임포트
from bson import ObjectId, json_util
from bson.errors import InvalidId
import hwp_processor  # HWP 파일 처리 모듈 임포트

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

@app.route('/api/extract-hwp', methods=['POST'])
def extract_hwp():
    request_data = request.get_json()
    file_path = request_data.get('filePath')
    try:
        content = hwp_processor.extract_text(file_path)
        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the News API", 200

@app.route('/news', methods=['GET'])
def get_news():
    news_items = list(news_collection.find({}, {'_id': 0}))
    return jsonify(news_items)

@app.route('/news', methods=['POST'])
def add_news():
    news_data = request.get_json()
    result = news_collection.insert_one(news_data)
    news_data['_id'] = str(result.inserted_id)
    return jsonify(news_data), 201

@app.route('/fetch-emails')
def fetch_emails():
    try:
        email_address = 'jys@pedien.com'
        password = '8IVI5wQNZ2hW'
        save_path = '/path_to_save_attachments'
        email_downloader.download_attachments(email_address, password, save_path)
        return jsonify({'status': 'success', 'message': 'Emails fetched and attachments downloaded'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/emails', methods=['GET'])
def get_emails():
    emails_json = fetch_emails_from_db()
    print(emails_json)
    return Response(emails_json, mimetype='application/json')

@app.route('/api/emails/<id>', methods=['GET'])
def get_email_detail(id):
    try:
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
