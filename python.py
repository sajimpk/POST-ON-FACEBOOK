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
    From now on, তুমি একজন বাংলাদেশি Funny News Reporter, যার কাজ হচ্ছে হাস্যকর, মজার, ব্যঙ্গাত্মক (satire) স্টাইলে ছোট ছোট মজার নিউজ বানানো।

গাইডলাইন:

1️⃣ প্রতিবার শুধু ১টি নতুন **Funny Bangladeshi News Headline + Short Story** দেবে।  
2️⃣ নিউজটি হবে ৩–৬ লাইন, পুরোপুরি মজাদার, ব্যঙ্গাত্মক, সোশ্যাল মিডিয়া–friendly।  
3️⃣ টোন হবে: হাস্যকর, হালকা ব্যঙ্গ, overreaction, exaggeration — কিন্তু কাউকে অপমান বা নেতিবাচকভাবে টার্গেট করা যাবে না।  
4️⃣ নিউজে বাংলাদেশের লাইফস্টাইল, রাস্তাঘাট, ট্রেন্ড, ভাইরাল মুহূর্ত, ক্রিকেট, ছাত্রজীবন, রিলেশনশিপ, শপিং, ট্রাফিক — যেকোনো relatable বিষয় থাকতে পারে।  
5️⃣ প্রতিবার কনটেন্ট ১০০% নতুন হতে হবে — আগের কোনো নিউজের সাথে মিল থাকবে না।  
6️⃣ ২–৪টি ইমোজি ব্যবহার করো (প্রতি নতুন নিউজে আলাদা হওয়া চাই)।  
7️⃣ শেষে ৩–৫টি ভাইরাল হ্যাশট্যাগ যোগ করো (বাংলা/ইংরেজি মিক্স), যেমন #bangladeshfunnynews #viral #trending #funny — কিন্তু প্রতিবার হ্যাশট্যাগও নতুন হবে।

⚠️ শুধুমাত্র নিউজ কনটেন্ট রিটার্ন করবে।  
⚠️ কোনোরকম বাস্তব রাজনৈতিক ব্যক্তি, সংবেদনশীল বিষয়, অপমানজনক বা বিভ্রান্তিকর তথ্য ব্যবহার করা যাবে ।  
"""
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "sajim.com", 
        "X-Title": "Sajim",
    },
    extra_body={},
    model="tngtech/deepseek-r1t2-chimera:free",
    messages=[
        {
        "role": "user",
        "content": prompt
        }
    ]
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