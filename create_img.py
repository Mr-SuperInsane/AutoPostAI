import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ["GPT_API"]

res = openai.Image.create(
    prompt="a girl, anime style, kawaii, painting by Alphonse Mucha, masterpiece, high quality, best quality, highly detailed, insanely detailed, 4K",
    n=1,
    size="1024x1024"
)

print(res)