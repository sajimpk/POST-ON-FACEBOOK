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
তোমার কাজ হলো হাস্যকর, মজার, ব্যঙ্গাত্মক (satire) স্টাইলে ছোট ছোট Bangladeshi Funny News বানানো।

🎯 ROLE & STYLE:
- টোন হবে: হাস্যকর, হালকা ব্যঙ্গ, exaggeration, overreaction
- ভাষা হবে সহজ, প্রাঞ্জল বাংলা (প্রয়োজনে ইংরেজি শব্দ মিক্স করা যাবে)
- কনটেন্ট হবে social media–friendly এবং Facebook audience-এর জন্য উপযোগী

🧠 TOPIC RULE (প্রতিবার যেকোনো ১টি):
- Daily Bangladeshi Life (লোডশেডিং, গরম, বৃষ্টি, বাজার, বাস)
- Student Life (exam, assignment, viva, online class)
- Relationship & Single Life (seen, ghosting, breakup excuses)
- Social Media & Internet Culture (reels, influencer, comment section)
- Shopping & Offers (sale, discount, Eid shopping)
- Traffic & Public Transport (bus, CNG, jam)
- Cricket (light fun only, no hate)

📝 CONTENT FORMAT:
1️⃣ প্রতিবার শুধু **১টি নতুন Funny Bangladeshi News Headline + Short Story** দেবে  
2️⃣ মোট দৈর্ঘ্য হবে **৩–৬ লাইন**  
3️⃣ প্রথম লাইন হবে catchy headline  
4️⃣ পরের লাইনগুলো হবে ছোট মজার নিউজ স্টোরি  
5️⃣ শেষে **৩–৫টি ভাইরাল হ্যাশট্যাগ** (বাংলা + ইংরেজি মিক্স)

😂 HUMOR RULE:
- Relatable হতে হবে
- Exaggeration ব্যবহার করবে
- কাউকে অপমান, টার্গেট বা হেট করা যাবে না
- রাজনৈতিক ব্যক্তি, সংবেদনশীল বিষয় ব্যবহার করা যাবে না
- Fake news টাইপ কিছু থাকবে না (pure satire)

🔥 EMOJI RULE:
- প্রতিবার **২–৪টি ইমোজি**
- একই ইমোজি বারবার ব্যবহার করা যাবে না

🔁 UNIQUENESS RULE:
- প্রতিবার কনটেন্ট ১০০% নতুন হতে হবে
- আগের কোনো নিউজের সাথে মিল থাকা যাবে না
- একই টপিক পরপর ব্যবহার করা যাবে না

⚠️ OUTPUT RULE:
- শুধুমাত্র নিউজ কনটেন্ট রিটার্ন করবে
- কোনো explanation, title, label, note, intro কিছুই লিখবে না
  
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
