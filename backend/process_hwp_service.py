from flask import Flask, request, jsonify
import hwp_processor  # hwp_processor.py의 함수를 import
import pymongo
import gridfs
import os

app = Flask(__name__)

def download_hwp_file_from_mongodb(file_id, save_path):
    client = pymongo.MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
    db = client['bounce']
    fs = gridfs.GridFS(db)

    file_data = fs.get(file_id).read()

    with open(save_path, 'wb') as f:
        f.write(file_data)

    return save_path

def process_hwp_file(file_path):
    title, subtitle, content = hwp_processor.analyze_content(file_path)
    return title, subtitle, content

def create_news_in_mongodb(title, subtitle, content, category='자동선택된 카테고리'):
    client = pymongo.MongoClient('mongodb+srv://username:password@cluster0.mongodb.net/')
    db = client['your_database']
    news_collection = db['news']

    news_data = {
        'title': title,
        'subtitle': subtitle,
        'content': content,
        'category': category,
        'author': '자동 작성자',
        'editor': '자동 편집자',
        'creationDate': '오늘 날짜',
        'updateDate': '오늘 날짜'
    }

    news_collection.insert_one(news_data)
    print("News data inserted successfully.")

@app.route('/process-hwp', methods=['POST'])
def process_hwp_file_endpoint():
    file_id = request.json.get('file_id')
    if not file_id:
        return jsonify({'error': 'No file ID provided'}), 400

    # 파일을 저장할 임시 경로 설정
    temp_file_path = 'temp_hwp_file.hwp'
    
    try:
        # MongoDB에서 파일 다운로드
        download_hwp_file_from_mongodb(file_id, temp_file_path)

        # HWP 파일 내용 추출
        title, subtitle, content = process_hwp_file(temp_file_path)

        # 뉴스 작성
        create_news_in_mongodb(title, subtitle, content)

        # 임시 파일 삭제
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return jsonify({'title': title, 'subtitle': subtitle, 'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


app = Flask(__name__)

@app.route('/process-hwp', methods=['POST'])
def process_hwp_file():
    """POST 요청으로 받은 파일 경로를 사용하여 HWP 파일을 처리합니다."""
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        title, subtitle, content = hwp_processor.analyze_content(file_path)
        return jsonify({'title': title, 'subtitle': subtitle, 'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == '__main__':
    app.run(debug=True)
