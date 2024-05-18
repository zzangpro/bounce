import os
from hwp5.filestructure import Hwp5File
import pymongo

def open_hwp(file_path):
    """HWP 파일을 열고 내용을 읽어 반환합니다."""
    try:
        hwp_file = Hwp5File(file_path)
        content = []
        for section in hwp_file.bodytext:
            for paragraph in section.paragraphs:
                text = ''.join(run.text for run in paragraph.text)
                content.append(text)
        return '\n'.join(content)
    except Exception as e:
        raise Exception(f"Error processing HWP file: {e}")

def extract_text(file_path):
    """HWP 파일에서 텍스트를 추출합니다."""
    try:
        text = open_hwp(file_path)
        return text
    except Exception as e:
        return str(e)

def fetch_emails_with_attachments():
    client = pymongo.MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
    db = client['bounce']
    emails_collection = db['emails']
    emails = emails_collection.find({'attachments': {'$exists': True, '$not': {'$size': 0}}})
    return emails

def process_email_attachments():
    emails = fetch_emails_with_attachments()
    for email in emails:
        for attachment in email['attachments']:
            file_path = attachment['path']  # 실제 파일 경로를 가져옵니다.
            content = extract_text(file_path)
            # 여기에서 내용을 분석하여 자동으로 제목, 부제목, 내용 등을 설정합니다.
            title, subtitle, content_text, category = analyze_content(content)
            # 뉴스 작성 및 저장 함수 호출
            create_news(title, subtitle, content_text, category)

def analyze_content(content):
    # 내용 분석 로직을 여기에 추가
    # 예를 들어, 첫 줄은 제목, 두 번째 줄은 부제목, 나머지는 내용으로 설정
    lines = content.split('\n')
    title = lines[0] if len(lines) > 0 else ''
    subtitle = lines[1] if len(lines) > 1 else ''
    content_text = '\n'.join(lines[2:]) if len(lines) > 2 else ''
    category = '자동선택된 카테고리'  # 내용에 따라 카테고리를 자동으로 설정하는 로직 추가
    return title, subtitle, content_text, category

def create_news(title, subtitle, content, category):
    client = pymongo.MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
    db = client['bounce']
    news_collection = db['news']
    news_data = {
        'title': title,
        'subtitle': subtitle,
        'content': content,
        'category': category,
        'author': '자동 작성자',  # 자동으로 작성한 것으로 설정
        'editor': '자동 편집자',
        'creationDate': '오늘 날짜',  # 날짜를 현재 날짜로 설정
        'updateDate': '오늘 날짜'
    }
    news_collection.insert_one(news_data)
    print("News data inserted successfully.")

if __name__ == "__main__":
    process_email_attachments()
