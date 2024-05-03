import logging
import imaplib
import email
from email.header import decode_header
import schedule
import time
from pymongo import MongoClient
import os
from email.mime.base import MIMEBase
import subprocess
from PIL import Image
import pytesseract


# 로그 기본 설정
logging.basicConfig(filename='email_downloader.log', level=logging.DEBUG, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# 사용 예시
logging.info("MongoDB connected successfully.")
logging.error("Failed to connect to MongoDB:", exc_info=True)

# MongoDB 설정
client = MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
db = client['bounce']
email_collection = db['emails']

# 데이터베이스 접속 상태 체크
try:
    # db.command('ping')을 사용하여 MongoDB 서버와의 연결을 확인합니다.
    db.command('ping')
    print("MongoDB connected successfully.")
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    
def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='kor+eng')  # 한국어 및 영어 인식
    return text
    
def extract_text_from_hwp(file_path):
    command = ['hwp5txt', file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

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
        print(f"Saved email: {subject}, ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to save email: {e}")

def download_emails():
    mail = None  # mail 객체 초기화
    try:
        mail = imaplib.IMAP4_SSL('imap.worksmobile.com', 993)
        mail.login('jys@pedien.com', '8IVI5wQNZ2hW')
        mail.select('inbox')
        status, messages = mail.search(None, 'ALL')
        messages = messages[0].split()

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
                        if bool(filename):
                            filepath = os.path.join('/path/to/save', filename)
                            with open(filepath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            attachment_files.append({'filename': filename, 'path': filepath})

                    save_email(subject, sender, date, has_attachments, attachment_files)
    except (imaplib.IMAP4.error, Exception) as e:
        print("Error connecting or processing email:", e)
    finally:
        if mail is not None:
            mail.logout()

schedule.every(1).minutes.do(download_emails)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
