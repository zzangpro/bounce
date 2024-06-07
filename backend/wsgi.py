import sys
import os

# 프로젝트 경로를 sys.path에 추가합니다.
path = '/home/bounce/mysite/flask_app.py'
if path not in sys.path:
    sys.path.append(path)

# 환경 변수를 설정하여 Flask 애플리케이션을 지정합니다.
os.environ['FLASK_APP'] = 'app.py'

# Flask 애플리케이션을 가져옵니다.
from app import app as application
