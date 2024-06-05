import hwp5
import olefile
import struct
import logging
import pymongo

logging.basicConfig(level=logging.DEBUG)


def test_mongodb_connection():
    try:
        client = pymongo.MongoClient('mongodb+srv://jyspress:LFC5XdWvhfJ3Io6s@cluster0.ninp3j8.mongodb.net/')
        db = client['bounce']
        logging.debug("MongoDB connection successful.")
        return True
    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
        return False
    
def extract_text(file_path):
    try:
        # HWP 파일을 읽고 처리합니다.
        hwp_doc = hwp5.parse(file_path)
        logging.debug(f"HWP file opened: {file_path}")

        # 문서 제목 추출
        title = hwp_doc.header.title if hwp_doc.header.title else "제목 없음"
        logging.debug(f"Extracted title: {title}")
        
        # BodyText 섹션의 내용 추출
        content = []
        for section in hwp_doc.bodytext.sections:
            for para in section.paragraphs:
                text = para.text.strip()
                content.append(text)
                logging.debug(f"Paragraph text: {text}")

        return title + "\n" + "\n".join(content)
    except Exception as e:
        logging.error(f"Error extracting HWP content: {e}")
        return str(e)

def extract_hwp_content(file_path):
    try:
        ole = olefile.OleFileIO(file_path)
        logging.debug(f"OLE file opened: {file_path}")

        for entry in ole.listdir():
            logging.debug(f"Stream entry: {entry}")

        if not ole.exists('PrvText'):
            raise Exception("PrvText stream not found in HWP file")

        encoded_text = ole.openstream('PrvText').read()
        text = encoded_text.decode('utf-16le', errors='ignore')
        logging.debug(f"PrvText stream decoded: {text[:100]}...")

        bodytext_streams = [entry for entry in ole.listdir() if entry[0].startswith('BodyText')]

        content = []
        for stream_name in bodytext_streams:
            stream = ole.openstream(stream_name).read()
            logging.debug(f"BodyText stream '{stream_name}' read with size {len(stream)} bytes")
            text_parts, font_sizes, bolds = parse_bodytext_stream(stream)
            content.extend(list(zip(text_parts, font_sizes, bolds)))

        # 디버깅: 추출한 텍스트와 폰트 크기 및 bold 정보를 출력합니다.
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
        # Block type indicator
        block_type = struct.unpack_from('<H', stream, pos)[0]
        pos += 2

        if block_type == 0x10:  # Paragraph header
            size = struct.unpack_from('<H', stream, pos)[0]
            pos += 2
            para_text = stream[pos:pos + size].decode('utf-16le', errors='ignore')
            text_parts.append(para_text)
            font_sizes.append(None)  # Placeholder, no font size info here
            bolds.append(False)  # Placeholder, no bold info here
            pos += size
        elif block_type == 0x50:  # Character shape
            size = struct.unpack_from('<H', stream, pos)[0]
            pos += 2
            font_size = struct.unpack_from('<H', stream, pos + 8)[0]  # Font size at offset 8
            is_bold = struct.unpack_from('<H', stream, pos + 4)[0] & 1  # Bold flag at offset 4
            font_sizes[-1] = font_size
            bolds[-1] = bool(is_bold)
            pos += size
        else:
            logging.debug(f"Unknown block type {block_type} at position {pos}")
            pos += 2  # Skip unknown block type

    return text_parts, font_sizes, bolds

def extract_title_and_content(content):
    title = "제목 없음"
    subtitle = ""
    content_text = []

    after_table = False
    for text, font_size, is_bold in content:
        logging.debug(f"Analyzing text: {text.strip()}, Font size: {font_size}, Bold: {is_bold}")
        if "표" in text:  # Assuming '표' indicates the table
            after_table = True
            continue

        if after_table:
            if font_size == 180 and is_bold:
                title = text.strip()
                logging.debug(f"Found title: {title}")
            elif font_size == 140:
                content_text.append(text.strip())
                logging.debug(f"Appending to content: {text.strip()}")

    logging.debug(f"Final extracted title: {title}")
    logging.debug(f"Final extracted content: {' '.join(content_text[:100])}...")
    return title, subtitle, '\n'.join(content_text)

def analyze_content(file_path):
    content = extract_hwp_content(file_path)
    if isinstance(content, str):
        return "제목 없음", "", content

    title, subtitle, full_content = extract_title_and_content(content)
    logging.debug(f"Extracted title: {title}, Content: {full_content[:100]}...")
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
    if test_mongodb_connection():
        print("MongoDB 연결이 성공적으로 이루어졌습니다.")
    else:
        print("MongoDB 연결에 실패했습니다.")
