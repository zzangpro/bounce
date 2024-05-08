from flask import Flask, request, jsonify
import hwp_processor  # 이 부분에서 hwp_processor.py의 함수를 import

app = Flask(__name__)

@app.route('/process-hwp', methods=['POST'])
def process_hwp_file():
    """POST 요청으로 받은 파일 경로를 사용하여 HWP 파일을 처리합니다."""
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        content = hwp_processor.extract_text(file_path)
        return jsonify({'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
