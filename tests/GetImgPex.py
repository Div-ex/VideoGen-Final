import os
from dotenv import load_dotenv
import requests


load_dotenv()

# Configuration
# PEXELS_API_KEY = os.getenv('PEXEL_API_KEY')

def fetch_pexels_images(keyword, num_images=1):
    """
    Fetch multiple images from Pexels for a given keyword.
    Return list of image URLs. If not enough images found, returns fewer.
    """
    # headers = {"Authorization": PEXELS_API_KEY}
    # params = {
    #     "query": keyword,
    #     "per_page": num_images,  
    #     "page": 1
    # }

    urls = ["https://miro.medium.com/v2/resize:fit:1024/1*-096_ftCtNsVP2JfpWeDgg.jpeg"]

    # try:
    #     response = requests.get("https://api.pexels.com/v1/search",
    #                             headers=headers,
    #                             params=params,
    #                             timeout=15)
    #     if response.status_code == 200:
    #         data = response.json()
    #         for photo in data.get('photos', []):
    #             urls.append(photo['src']['large'])
    #     return urls
    # except Exception as e:
        # logging.error(f"Image fetch error: {str(e)}")
    return urls