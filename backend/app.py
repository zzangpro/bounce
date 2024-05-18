from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import hwp_processor  # HWP 파일 처리 모듈 임포트
from pymongo import MongoClient
from bson import ObjectId, json_util

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 모든 경로에 대해 모든 도메인 허용


# MongoDB Atlas 연결
client = MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
db = client['bounce']
news_collection = db['news']
emails_collection = db['emails']
categories_collection = db['categories']

@app.route('/api/process-hwp', methods=['POST'])
def process_hwp():
    try:
        # MongoDB에서 가장 최근의 이메일을 가져옵니다.
        email = emails_collection.find_one(sort=[('_id', -1)])
        if not email or 'attachments' not in email or not email['attachments']:
            return jsonify({'error': 'No email attachments found'}), 404

        # 첨부파일 경로 설정 (예제에서는 첫 번째 첨부파일을 처리)
        attachment = email['attachments'][0]
        attachment_path = attachment['path']  # 올바른 키를 사용하여 경로를 가져옴

        # 로그 추가: 경로 확인
        print(f"Processing HWP file at path: {attachment_path}")

        # HWP 파일 처리
        if not os.path.exists(attachment_path):
            return jsonify({'error': f'File not found: {attachment_path}'}), 404

        content = hwp_processor.extract_text(attachment_path)
        title, subtitle, content_text, category = hwp_processor.analyze_content(content)
        data = {
            'title': title,
            'subtitle': subtitle,
            'content': content_text,
            'category': category
        }
        return jsonify(data), 200
    except Exception as e:
        # 로그 추가: 에러 메시지 출력
        print(f"Error processing HWP file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the News API", 200

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list(categories_collection.find({}, {'_id': 0}))
    if not categories:
        return jsonify({'error': 'No categories found'}), 404
    return jsonify(categories), 200

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

@app.route('/api/news/data', methods=['GET'])
def get_news_data():
    # news 데이터를 가져오는 로직을 여기에 추가
    # 예시로 news_collection의 첫 번째 문서를 반환하도록 합니다.
    news_data = news_collection.find_one()
    if not news_data:
        return jsonify({'error': 'No news data found'}), 404
    return jsonify({
        'title': news_data.get('title', ''),
        'subtitle': news_data.get('subtitle', ''),
        'content': news_data.get('content', ''),
        'image': news_data.get('image', '')
    }), 200

@app.route('/fetch-emails')
def fetch_emails():
    try:
        email_address = 'jys@pedien.com'
        password = '8IVI5wQNZ2hW'
        save_path = '/path_to_save_attachments'
        email_downloader.download_attachments(email_address, password, save_path)
        return jsonify({'status': 'success', 'message': 'Emails fetched and attachments downloaded'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/emails', methods=['GET'])
def get_emails():
    emails = list(emails_collection.find({}))
    return Response(json_util.dumps(emails), mimetype='application/json')

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
