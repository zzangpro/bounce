from pymongo import MongoClient
import pymongo

import pymongo

# MongoDB Atlas 연결
client = pymongo.MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
db = client['bounce']
categories_collection = db['categories']

# 카테고리 데이터
categories_data = {
    'category1': [
        {'id': '101', 'name': 'Seoul'},
        {'id': '102', 'name': 'Busan'},
        # 추가 카테고리1 데이터
    ],
    'category2': [
        {'id': '201', 'name': 'Education'},
        {'id': '202', 'name': 'Technology'},
        # 추가 카테고리2 데이터
    ],
    'category3': [
        {'id': '301', 'name': 'Politics'},
        {'id': '302', 'name': 'Economy'},
        # 추가 카테고리3 데이터
    ],
    'category4': [
        {'id': '401', 'name': 'Health'},
        {'id': '402', 'name': 'Environment'},
        # 추가 카테고리4 데이터
    ]
}

# 기존 데이터 삭제
categories_collection.delete_many({})

# 카테고리 데이터 삽입
categories_collection.insert_one(categories_data)
print("Categories data inserted successfully.")

