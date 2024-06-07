import logging
import imaplib
import email
from email.header import decode_header
import schedule
import time
from pymongo import MongoClient
import gridfs
import os
import re
import urllib.parse
from bson import ObjectId

# 로그 기본 설정
logging.basicConfig(filename='email_downloader.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# MongoDB 설정
client = MongoClient('mongodb://jyspress:LFC5XdWvhfJ3Io6s@ac-sen5mzo-shard-00-00.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-01.ninp3j8.mongodb.net:27017,ac-sen5mzo-shard-00-02.ninp3j8.mongodb.net:27017/bounce?ssl=true&replicaSet=atlas-1rvho8-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client['bounce']
email_collection = db['emails']
fs = gridfs.GridFS(db)
fs_files_collection = db['fs.files']

# 로그 파일 경로
log_file_path = 'D:/path/to/email_download.log'

def check_file_in_gridfs(file_id):
    # GridFS에서 파일 ID 확인
    result = fs_files_collection.find_one({"_id": ObjectId(file_id)})
    return result is not None

def decode_filename(encoded_filename):
    try:
        decoded_filename = urllib.parse.unquote(encoded_filename)
        return decoded_filename.encode('latin1').decode('utf-8')
    except (UnicodeDecodeError, TypeError):
        return encoded_filename

def parse_log_file_and_check_ids(log_file_path):
    # 파일 ID를 저장할 리스트 초기화
    file_ids = []

    # 정규 표현식 패턴
    no_file_pattern = re.compile(r'No file found in GridFS with id: (.+)')
    saved_file_pattern = re.compile(r'Attachment saved: (.+), file_id: (.+)')

    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            no_file_match = no_file_pattern.search(line)
            if no_file_match:
                file_id = no_file_match.group(1).strip()
                file_ids.append(file_id)
            
            saved_file_match = saved_file_pattern.search(line)
            if saved_file_match:
                encoded_filename = saved_file_match.group(1).strip()
                file_id = saved_file_match.group(2).strip()
                decoded_filename = decode_filename(encoded_filename)
                logging.info(f"Original Filename: {encoded_filename}, Decoded Filename: {decoded_filename}, File ID: {file_id}")
    
    # MongoDB에서 파일 ID 확인
    for file_id in file_ids:
        exists = check_file_in_gridfs(file_id)
        if exists:
            print(f"File ID {file_id} exists in GridFS.")
        else:
            print(f"File ID {file_id} does not exist in GridFS.")

# 데이터베이스 접속 상태 체크
try:
    db.command('ping')
    logging.info("MongoDB connected successfully.")
except Exception as e:
    logging.error("Failed to connect to MongoDB:", exc_info=True)

def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf-8') if isinstance(word, bytes) else word
        for word, encoding in decode_header(s))

def clean_filename(filename):
    filename = decode_mime_words(filename)
    filename = re.sub(r'[\\/*?:"<>|]', '', filename)
    return filename

def save_email(subject, sender, date, has_attachments, attachment_files):
    email_data = {
        'subject': subject,
        'sender': sender,
        'date': date,
        'has_attachments': has_attachments,
        'attachments': attachment_files
    }
    try:
        result = email_collection.insert_one(email_data)
        logging.info(f"Saved email: {subject}, ID: {result.inserted_id}")
        logging.info(f"Email data: {email_data}")
    except Exception as e:
        logging.error(f"Failed to save email: {e}")

def download_emails():
    mail = None
    try:
        mail = imaplib.IMAP4_SSL('imap.worksmobile.com', 993)
        mail.login('jys@pedien.com', '8IVI5wQNZ2hW')
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        messages = messages[0].split()
        messages.reverse()

        for msg_id in messages:
            res, msg = mail.fetch(msg_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8', errors='replace')
                    sender = msg.get('from')
                    date = msg.get('date')
                    attachment_files = []
                    has_attachments = False

                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        
                        has_attachments = True
                        filename = part.get_filename()
                        if filename:
                            filename = clean_filename(filename)
                            file_data = part.get_payload(decode=True)
                            
                            try:
                                file_id = fs.put(file_data, filename=filename)
                                decoded_filename = decode_filename(filename)
                                attachment_files.append({'filename': decoded_filename, 'file_id': str(file_id)})  # file_id를 문자열로 변환하여 저장
                                logging.info(f"Attachment saved: {decoded_filename}, file_id: {file_id}")
                            except Exception as e:
                                logging.error(f"Cannot save file to MongoDB: {e}")

                    save_email(subject, sender, date, has_attachments, attachment_files)
    except (imaplib.IMAP4.error, Exception) as e:
        logging.error("Error connecting or processing email:", exc_info=True)
    finally:
        if mail is not None:
            mail.logout()
            
def job():
    parse_log_file_and_check_ids(log_file_path)
    
if __name__ == "__main__":
    # 스케줄 설정: 매 1분마다 job 함수 실행
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
