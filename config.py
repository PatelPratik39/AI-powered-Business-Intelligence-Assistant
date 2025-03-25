import os
from dotenv import load_dotenv

def laod_api_key():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")