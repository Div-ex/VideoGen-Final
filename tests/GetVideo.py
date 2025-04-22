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
from tests.GenText import generate_script, parse_script
from tests.GetImgPex import fetch_pexels_images

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
        img = Image.open(BytesIO(response.content)).convert("RGB")
        
        # Resize with aspect ratio preserved, then pad with black to fit target resolution
        img.thumbnail(resolution, Image.Resampling.LANCZOS)  # Resize while keeping aspect ratio

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

        # output_filename = "final_video.mp4"
        # final_clip.write_videofile(output_filename, fps=1, codec='libx264', audio_codec='aac')

            # Add 1-second black gap between clips
        gap_clip = ColorClip(size=resolution, color=(0, 0, 0), duration=1)
        clips_with_gaps = []

        for clip in all_clips:
            clips_with_gaps.append(clip)
            clips_with_gaps.append(gap_clip)

        # Remove the last gap
        if clips_with_gaps:
            clips_with_gaps = clips_with_gaps[:-1]

        final_clip = concatenate_videoclips(clips_with_gaps, method="compose")

        # Save with a timestamp-based unique filename
        import time
        timestamp = int(time.time())
        output_filename = f"final_video_{timestamp}.mp4"
        final_clip.write_videofile(
            output_filename,
            fps=1,
            codec='libx264',
            audio_codec='aac',
            ffmpeg_params=["-pix_fmt", "yuv420p"]
        )

        return output_filename

    except Exception as e:
        logging.error(f"Video generation error: {str(e)}")
        return None