from create_gpt import create_content, create_headline, create_title, create_tweet_content
import markdown
import json
import requests
import tweepy
import os
from dotenv import load_dotenv
from random import choice
load_dotenv()

CONTENT = 'CPU'
CATEGORY = 'パソコン'

category_dict = {'パソコン':[4], 'スマホ/タブレット':[1], 'オーディオ':[6,10], 'キーボード':[8,6] , 'マウス':[9,6], 'その他':[11]}
img_id = [247,246,245,244,243,242,241,240,239,238,237,236,235,234,233,232,231,230,229,228,227,226,225,224,223,222,164,134,101,70,65,51]

def tweet(content):
    ck = os.environ["CONSUMER_KEY"]
    cs = os.environ["CONSUMER_SECRET_KEY"]
    at = os.environ["ACCESS_TOKEN"]
    ats = os.environ["ACCESS_SECRET_TOKEN"]

    try:
        client = tweepy.Client(consumer_key=ck, consumer_secret=cs, access_token=at, access_token_secret=ats)
        res = client.create_tweet(text=content)
        res = res.data
        return res["id"]
    except:
        return "error"



title_list = create_title(theme=CONTENT)
for i, title in enumerate(title_list):
    print(f'No.{i+1}の記事を執筆しています')
    headline_list = create_headline(title)
    # 内容をすべて関数内で生成
    md = create_content(title, headline_list)
    html = markdown.markdown(md)
    status = 'publish'
    img = choice(img_id)
    payload = {'title': title ,'content' : html ,'status' : status, 'categories': category_dict[CATEGORY], 'featured_media':img}
    headers = {'content-type': "Application/json"}
    # 環境変数 未実行
    r = requests.post("https://YOUR_BLOG_URL/wp-json/wp/v2/posts", data=json.dumps(payload) , headers=headers, auth=('YOUR_WORDPRESS_USER_NAME', 'YOUR_WORDPRESS_API_TOKEN') )
    if str(r) != '<Response [201]>':
        print(f'タイトル「{title}」の投稿に失敗しました')
    else:
        print(f'タイトル「{title}」の投稿に成功しました')
        post_url = r.json()['guid']['rendered']
        # ツイート文作成
        text = f'「{title}」というタイトルのブログ記事を作成しました。見出しは'
        for headline in headline_list:
            text += f'「{headline}」'
        text += 'です。このブログ記事を宣伝するためのツイート文を作成してください。'
        tweet_text = create_tweet_content(text)
        tweet_text += f'\n\n{post_url}'
        res = tweet(tweet_text)
        if res != "error":
            print('ツイートに成功しました')

        