import time
from dotenv import load_dotenv
import os
from bot import filter_messages

# Load .env variables
load_dotenv()

username = os.getenv('INSTA_USERNAME')
password = os.getenv('INSTA_PASSWORD')

while True:
    filter_messages(username, password)
    time.sleep(5)