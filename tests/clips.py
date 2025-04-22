from gtts import gTTS
from moviepy.editor import *
import requests
from PIL import Image
import numpy as np
import textwrap
import logging
from io import BytesIO

def create_clip_from_image(image_url, text, output_audio_path="temp_audio.mp3"):
    """
    Create a single video clip from one image URL, with text overlay and TTS audio narration.
    The duration of the clip is determined by the length of the generated audio narration.
    """
    try:
        # Generate TTS audio
        tts = gTTS(text)
        tts.save(output_audio_path)
        audio_clip = AudioFileClip(output_audio_path)
        duration = audio_clip.duration  # Set video duration based on audio duration

        # Fetch image
        response = requests.get(image_url, timeout=15)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((1280, 720))
        img_np = np.array(img)
        
        # Create video clip
        clip = ImageClip(img_np).set_duration(duration)

        # Create text overlay
        wrapped_text = textwrap.fill(text, width=40)
        txt_clip = TextClip(
            wrapped_text,
            fontsize=28,
            color="white",
            font="DejaVu-Sans-Bold",
            method="caption",
            align="center",
            stroke_color="black",
            stroke_width=2
        ).set_duration(duration).set_position(("center", "bottom"))
        
        # Combine video and text overlay
        video_clip = CompositeVideoClip([clip, txt_clip])
        
        # Set audio narration to video
        video_clip = video_clip.set_audio(audio_clip)
        
        video_clip.write_videofile("output_v.mp4", fps=24, codec='h264_nvenc', audio_codec='aac')

        # return video_clip
    except Exception as e:
        logging.error(f"Clip creation from image failed: {str(e)}")
        return None

create_clip_from_image("https://cdn.motor1.com/images/mgl/1ZEpmp/s1/pagani-zonda-760-roadster-diamante-verde.jpg", "This is a Pagani Zonda supercar. It is a limited-production sports car manufactured by the Italian automobile manufacturer Pagani. The Zonda was first introduced in 1999 and has undergone several updates and special editions over the years.")