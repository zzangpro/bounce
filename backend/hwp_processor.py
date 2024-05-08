from pyhwp import hwp5

def open_hwp(file_path):
    """HWP 파일을 열고 내용을 읽어 반환합니다."""
    try:
        hwp_file = hwp5.open(file_path)
        content = hwp_file.read_text()
        return content
    except Exception as e:
        raise Exception(f"Error processing HWP file: {e}")

def extract_text(file_path):
    """HWP 파일에서 텍스트를 추출합니다."""
    try:
        text = open_hwp(file_path)
        return text
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # 파일 경로를 입력받아 테스트
    import sys
    file_path = sys.argv[1] if len(sys.argv) > 1 else 'example.hwp'
    print(extract_text(file_path))
