import os
from dotenv import load_dotenv
import requests

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')
load_dotenv()

# Configuration
PEXELS_API_KEY = os.getenv('PEXEL_API_KEY_2')

def extract_keyword(text):
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    return keywords[0] if keywords else "nature"

def fetch_pexels_images(keyword, num_images=1):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": num_images, "page": 1, "orientation" : "landscape", "size" : "small"}
    try:
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=10)
        data = response.json()
        return [photo['src']['large'] for photo in data.get('photos', [])]
    except:
        return []

# def fetch_pexels_images(keyword, num_images=1):
#     """
#     Fetch multiple images from Pexels for a given keyword.
#     Return list of image URLs. If not enough images found, returns fewer.
#     """
#     headers = {"Authorization": PEXELS_API_KEY}
#     params = {
#         "query": keyword,
#         "per_page": num_images,  
#         "page": 1
#     }

#     urls = []

#     try:
#         response = requests.get("https://api.pexels.com/v1/search",
#                                 headers=headers,
#                                 params=params,
#                                 timeout=15)
#         if response.status_code == 200:
#             data = response.json()
#             for photo in data.get('photos', []):
#                 urls.append(photo['src']['large'])
#         return urls
#     except Exception as e:
#         # logging.error(f"Image fetch error: {str(e)}")
#         return urls