import os
from hwp5.filestructure import Hwp5File
import pymongo
import logging

logging.basicConfig(level=logging.DEBUG)

def open_hwp(file_path):
    """HWP 파일을 열고 내용을 읽어 반환합니다."""
    try:
        hwp_file = Hwp5File(file_path)
        content = []
        logging.debug(f"Opened HWP file: {file_path}")
        
        for section in hwp_file.bodytext:
            if hasattr(section, 'paragraphs'):
                for paragraph in section.paragraphs:
                    paragraph_text = []
                    if hasattr(paragraph, 'text'):
                        for run in paragraph.text:
                            if hasattr(run, 'text'):
                                paragraph_text.append(run.text)
                            else:
                                paragraph_text.append(run)
                    else:
                        paragraph_text.append(str(paragraph))
                    content.append(''.join(paragraph_text))
            else:
                content.append(str(section))

        return '\n'.join(content)
    except Exception as e:
        logging.error(f"Error processing HWP file: {e}")
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
            file_path = attachment['path']
            content = extract_text(file_path)
            title, subtitle, content_text = analyze_content(content)
            category = '자동선택된 카테고리'
            create_news(title, subtitle, content_text, category)

def analyze_content(content):
    lines = content.split('\n')
    title = lines[0] if len(lines) > 0 else ''
    subtitle = lines[1] if len(lines) > 1 else ''
    content_text = '\n'.join(lines[2:]) if len(lines) > 2 else ''
    category = '자동선택된 카테고리'
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
        'author': '자동 작성자',
        'editor': '자동 편집자',
        'creationDate': '오늘 날짜',
        'updateDate': '오늘 날짜'
    }
    news_collection.insert_one(news_data)
    logging.debug("News data inserted successfully.")

if __name__ == "__main__":
    process_email_attachments()
