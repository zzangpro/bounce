from olefile import OleFileIO
import struct
import logging
import pymongo

logging.basicConfig(level=logging.DEBUG)

def extract_hwp_content(file_path):
    try:
        ole = OleFileIO(file_path)
        if not ole.exists('PrvText'):
            raise Exception("PrvText stream not found in HWP file")

        encoded_text = ole.openstream('PrvText').read()
        text = encoded_text.decode('utf-16le', errors='ignore')

        bodytext_streams = [entry for entry in ole.listdir() if entry[0].startswith('BodyText')]

        content = []
        for stream_name in bodytext_streams:
            stream = ole.openstream(stream_name).read()
            text_parts, font_sizes, bolds = parse_bodytext_stream(stream)
            content.extend(list(zip(text_parts, font_sizes, bolds)))

        # 디버깅: 추출한 텍스트와 폰트 크기를 출력합니다.
        for part in content:
            logging.debug(f"Text: {part[0]}, Font size: {part[1]}, Bold: {part[2]}")

        return content
    except Exception as e:
        logging.error(f"Error extracting HWP content: {e}")
        return str(e)

def parse_bodytext_stream(stream):
    pos = 0
    text_parts = []
    font_sizes = []
    bolds = []

    while pos < len(stream):
        if stream[pos:pos+2] == b'\x10\x00':  # Paragraph header
            pos += 2
            size = struct.unpack_from('<H', stream, pos)[0]
            pos += 2
            para_text = stream[pos:pos+size].decode('utf-16le', errors='ignore')
            text_parts.append(para_text)
            font_sizes.append(None)  # Placeholder, no font size info here
            bolds.append(False)  # Placeholder, no bold info here
            pos += size
        elif stream[pos:pos+2] == b'\x50\x00':  # Character shape
            pos += 2
            size = struct.unpack_from('<H', stream, pos)[0]
            pos += 2
            font_size = struct.unpack_from('<H', stream, pos + 8)[0]  # Font size at offset 8
            is_bold = struct.unpack_from('<H', stream, pos + 4)[0] & 1  # Bold flag at offset 4
            font_sizes[-1] = font_size
            bolds[-1] = bool(is_bold)
            pos += size
        else:
            pos += 2

    return text_parts, font_sizes, bolds

def extract_title_and_content(content):
    title = "제목 없음"
    subtitle = ""
    content_text = []

    after_table = False
    for text, font_size, is_bold in content:
        logging.debug(f"Analyzing text: {text}, font size: {font_size}, bold: {is_bold}")
        if "표" in text:  # Assuming '표' indicates the table
            after_table = True
            continue

        if after_table:
            if font_size == 180 and is_bold:
                title = text.strip()
            elif font_size == 140:
                content_text.append(text.strip())

    return title, subtitle, '\n'.join(content_text)

def analyze_content(file_path):
    content = extract_hwp_content(file_path)
    if isinstance(content, str):
        return "제목 없음", "", content

    title, subtitle, full_content = extract_title_and_content(content)
    logging.debug(f"Extracted title: {title}, content: {full_content[:100]}...")  # 내용이 길면 일부만 출력
    return title, subtitle, full_content

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
            title, subtitle, content_text = analyze_content(file_path)
            category = '자동선택된 카테고리'
            create_news(title, subtitle, content_text, category)

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
