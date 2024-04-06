# backend/app.py

from flask import Flask, jsonify

app = Flask(__name__)

# 테스트용 데이터
mock_data = [
    {'id': 1, 'title': 'First item', 'description': 'This is the first item'},
    {'id': 2, 'title': 'Second item', 'description': 'This is the second item'}
]

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(mock_data)

if __name__ == '__main__':
    app.run(debug=True)
