import requests
import json
import pymongo
import gridfs
import os
import olefile
import zipfile

def is_valid_hwp(file_path):
    try:
        with olefile.OleFileIO(file_path) as ole:
            if ole.exists('BodyText'):
                return True
        return False
    except:
        return False

def download_file_from_mongodb(file_id, save_path):
    client = pymongo.MongoClient('mongodb://jyspress:LFC5XdWvhfJ3Io6s@ac-sen5mzo-shard-00-00.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-01.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-02.ninp3j8.mongodb.net:27017/bounce?ssl=true&replicaSet=atlas-1rvho8-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['bounce']
    fs = gridfs.GridFS(db)

    try:
        file_data = fs.get(file_id).read()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(file_data)
        print(f'File downloaded and saved to {save_path}')
    except gridfs.errors.NoFile:
        print(f"No file found in GridFS with id: {file_id}")

def send_hwp_processing_request(file_path):
    url = 'http://127.0.0.1:5000/process-hwp'
    data = {'file_path': file_path}
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200:
        try:
            response_json = response.json()
            print('HWP 파일 처리 성공:', response_json)
        except json.JSONDecodeError:
            print('HWP 파일 처리 성공: 빈 응답을 받았습니다.')
    else:
        try:
            response_json = response.json()
            print('HWP 파일 처리 실패:', response_json)
        except json.JSONDecodeError:
            print('HWP 파일 처리 실패: 빈 응답을 받았습니다.')

def process_image_file(file_path):
    print(f"Processing image file: {file_path}")
    # 이미지 파일 처리 로직 추가 가능

def extract_and_process_zip(file_path, temp_dir):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            extracted_file_path = os.path.join(root, file)
            if file.endswith('.hwp'):
                if is_valid_hwp(extracted_file_path):
                    send_hwp_processing_request(extracted_file_path)
                else:
                    print(f"Invalid HWP file: {extracted_file_path}")
            elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                process_image_file(extracted_file_path)
            else:
                print(f"Unsupported file type: {extracted_file_path}")

def fetch_emails_with_attachments():
    client = pymongo.MongoClient('mongodb://jyspress:LFC5XdWvhfJ3Io6s@ac-sen5mzo-shard-00-00.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-01.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-02.ninp3j8.mongodb.net:27017/bounce?ssl=true&replicaSet=atlas-1rvho8-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client['bounce']
    emails_collection = db['emails']
    emails = emails_collection.find({'attachments': {'$exists': True, '$not': {'$size': 0}}})
    return emails

def process_email_attachments():
    emails = fetch_emails_with_attachments()
    for email in emails:
        for attachment in email['attachments']:
            if 'file_id' in attachment:
                file_id = attachment['file_id']
                filename = attachment['filename']
                save_path = f'D:/actual/path/to/{filename}'
                download_file_from_mongodb(file_id, save_path)
                
                if filename.endswith('.hwp'):
                    if is_valid_hwp(save_path):
                        send_hwp_processing_request(save_path)
                    else:
                        print(f"Invalid HWP file: {save_path}")
                elif filename.endswith('.zip'):
                    temp_dir = os.path.splitext(save_path)[0]  # Create a directory named after the zip file (without extension)
                    os.makedirs(temp_dir, exist_ok=True)
                    extract_and_process_zip(save_path, temp_dir)
                elif filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    process_image_file(save_path)
                else:
                    print(f"Unsupported file type: {filename}")
            else:
                print(f"No file_id found for attachment: {attachment}")

if __name__ == "__main__":
    process_email_attachments()
