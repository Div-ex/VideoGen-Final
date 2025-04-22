
import logging
from PIL import Image

import requests
import numpy as np
from PIL import Image
from gtts import gTTS
from moviepy.editor import *
import textwrap
from io import BytesIO
import logging

import requests

import os
from dotenv import load_dotenv
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


load_dotenv()

import ollama
import requests
import re
import logging



def generate_script(prompt):
    try:
        result = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'system',
                'content': """Give me ten lines on this topic. They should not be numbered""",
            },
            {
                'role': 'user',
                'content': prompt,
            },
        ])
#        
        print(result['message']['content'])
        return result['message']['content']
    except Exception as e:
        return f"Exception occurred: {str(e)}"


def parse_script(output):
    """
    Parse plain paragraph text and extract a list of script lines (text only).
    Each sentence is considered one script line.
    """
    if not output:
        return [], []

    keywords = []  # Placeholder for future keyword extraction if needed

    # Use regular expression to split on sentence boundaries (., ?, !)
    sentences = re.split(r'(?<=[.!?])\s+', output.strip())
    script = [sentence.strip() for sentence in sentences if sentence.strip()]
    print(script)
    return script


# parse_script(generate_script("World war 2"))


# Configuration
PEXELS_API_KEY = os.getenv('PEXEL_API_KEY_')

def extract_keyword(text):
    tokens = word_tokenize(text.lower())
    keywords = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    return keywords[0] if keywords else "nature"

def fetch_pexels_images(keyword, num_images=1):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": num_images, "page": 1}
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

logging.basicConfig(level=logging.INFO)


def create_clip_from_image(scene_text, images_per_scene = 1, output_audio_path="temp_audio.mp3", resolution = (854, 480)):
    """
    Create a single video clip from one image URL, with text overlay and TTS audio narration.
    The duration of the clip is determined by the length of the generated audio narration.
    """
    
    if scene_text:
        primary_keyword = scene_text
    else:
        primary_keyword = "nature"  

    
    image_url = fetch_pexels_images(primary_keyword, num_images=images_per_scene)

    if not image_url:
        logging.warning(f"No images found for {primary_keyword}, using fallback.")
        return [ColorClip(size=resolution, color=(0,0,0), duration=duration)]
    
    try:
        # Generate TTS audio
        text = scene_text
        tts = gTTS(text)
        tts.save(output_audio_path)
        audio_clip = AudioFileClip(output_audio_path)
        duration = audio_clip.duration  # Set video duration based on audio duration

        # Fetch image
        response = requests.get(image_url[0], timeout=15)
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB") 
        
        # Resize with aspect ratio preserved, then pad with black to fit target resolution
        img.thumbnail(resolution, Image.ANTIALIAS)  # Resize while keeping aspect ratio

        # Create black background
        background = Image.new('RGB', resolution, (0, 0, 0))
        offset = (
            (resolution[0] - img.width) // 2,
            (resolution[1] - img.height) // 2
        )
        background.paste(img, offset)

        img_np = np.array(background)
        clip = ImageClip(img_np).set_duration(duration)

        # img = img.resize(resolution)  # Resize to 854x480 for better performance
        # img_np = np.array(img)
        
        # # Create video clip
        # clip = ImageClip(img_np).set_duration(duration)

        # Create text overlay
        wrapped_text = textwrap.fill(text, width=50)
        txt_clip = TextClip(
            wrapped_text,
            fontsize=30,
            color="white",
            font="Arial",
            method="label",
            # align="center",
            stroke_color="black",
            stroke_width=1,
        ).set_duration(duration).set_position(("center", "bottom"))
        
        # Combine video and text overlay
        video_clip = CompositeVideoClip([clip, txt_clip])
        
        # Set audio narration to video
        video_clip = video_clip.set_audio(audio_clip)
        

        return video_clip
    except Exception as e:
        logging.error(f"Clip creation from image failed: {str(e)}")
        return None
    
def generate_video(prompt, images_per_scene=1, resolution=(1280, 720)):
    """
    Full pipeline:
      1) Generate script (approx 60s)
      2) Parse it
      3) For each scene, fetch images, create subclips with crossfade
      4) Concatenate scene clips with crossfade
      5) Generate TTS, overlay final audio
      6) Write final video to disk
    """
    try:
        raw_script = generate_script(prompt)
        if not raw_script:
            logging.error("No script generated.")
            return None

        script = parse_script(raw_script)
        if not script:
            logging.error("No valid scenes in script.")
            logging.info(f"Parsed script: {script}")
            return None
        print(script)
        for scene_text in script:
            print("gen_vid",scene_text)
        
        all_clips = []
        for scene_text in script:
            scene_clips = create_clip_from_image(
                scene_text=scene_text,
                # duration=duration,
                # keywords=keywords,
                images_per_scene=images_per_scene,
                resolution=resolution,
            )
            # print("gen_vid",scene_text)
            if not scene_clips:
                logging.error(f"Scene clips for '{scene_text}' are None.")
                continue 
 
            # scene_clips = scene_clips.crossfadein(1.0)
            all_clips.append(scene_clips)
        final_clip = concatenate_videoclips(all_clips, method="compose", padding=-1)

        output_filename = "final_video.mp4"
        final_clip.write_videofile(output_filename, fps=1, codec='libx264', audio_codec='aac')

        return output_filename
    except Exception as e:
        logging.error(f"Video generation error: {str(e)}")
        return None


if __name__ == "__main__":
    user_prompt = "History of Generative AI"
    video_file = generate_video(user_prompt, images_per_scene=1, resolution=(1920, 1080))

    if video_file:
        print("\nVideo generated successfully!")
       
    else:
        print("\nVideo generation failed. Check error logs above.")