from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Base config class."""
    APIKEY = os.environ.get('APIKEY')
    LAT = os.environ.get('LAT') 
    LONG = os.environ.get('LONG')
