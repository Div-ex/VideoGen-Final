from components.GetVideo import generate_video

if __name__ == "__main__":
    user_prompt = "History of Generative AI"
    video_file = generate_video(user_prompt, images_per_scene=1, resolution=(1920, 1080))

    if video_file:
        print("\nVideo generated successfully!")
       
    else:
        print("\nVideo generation failed. Check error logs above.")