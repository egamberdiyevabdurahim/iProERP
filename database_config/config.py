import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DB_CONFIG = {
    'database': DB_NAME,
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT,
}


TOKEN = os.getenv('TOKEN')

GROUP_ID = os.getenv('GROUP_ID')
MOVIE_DATA_GROUP_ID = os.getenv('MOVIE_DATA_GROUP_ID')

DEVELOPER_ID = os.getenv('DEVELOPER_ID')
ADMIN_ID = os.getenv('ADMIN_ID')