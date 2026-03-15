import requests
from openai import OpenAI
import os
from dotenv import load_dotenv
import random
# Load env variables
load_dotenv()
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME =os.getenv("CHANNEL_USERNAME")  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


Base_URL = "https://openrouter.ai/api/v1"
client = OpenAI(
  base_url= Base_URL,
  api_key = OPENAI_API_KEY
) 


def format_post(text):
    
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    headline = lines[0]
    story_lines = []
    hashtags = []

    # Separate story + hashtags
    for line in lines[1:]:
        if line.startswith("#"):
            hashtags.append(line)
        else:
            story_lines.append(line)

    # Join story paragraph
    story = "\n".join(story_lines)

    # Hashtags clean format
    hashtags_text = " ".join(hashtags)

    final_post = (
        f"🔥 {headline}\n\n"
        f"{story}\n\n"
        f"{hashtags_text}"
    )

    return final_post


def generate_post():
    prompt = """
    From now on, তুমি একজন বাংলাদেশি Funny News Reporter।
    তোমার কাজ হলো হাস্যকর, মজার, ব্যঙ্গাত্মক স্টাইলে ছোট Bangladeshi Funny News বানানো।

    3-6 lines
    first line headline
    end with 3-5 hashtags
    """

    completion = client.chat.completions.create(
        model="openrouter/hunter-alpha",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.9,
        max_tokens=150
    )

    message = completion.choices[0].message.content
    final_text = format_post(message)

    return final_text

def post_to_facebook(message, image_path=None):
    if image_path:
        url = f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
        payload = {
            "message": message,
            "access_token": FB_ACCESS_TOKEN,
            "published": "true"
        }
        files = {
            "source": open(image_path, "rb")
        }
        response = requests.post(url, data=payload, files=files)
    else:
        # Only text post
        url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
        payload = {"message": message, "access_token": FB_ACCESS_TOKEN}
        response = requests.post(url, data=payload)

    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        message = generate_post()
        number = random.randint(1, 10)
        result = post_to_facebook(message, image_path=f"image/{number}.jpg")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print(" ")
