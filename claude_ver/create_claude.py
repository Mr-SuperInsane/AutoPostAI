# -*- coding: utf-8 -*-
from claude_api import Client
import markdown

# タイトル作成
def title(content):
    claude_api = Client('CLAUDE_PAGE_SESSION_DATA')
    conversation_id = "CLAUDE_PAGE_URL_ID"

    # 生成する記事数を指定
    prompt = f'''{content}に関するブログ記事のタイトルを下記の項目に注意して2個考案してください。
    ・文字数それぞれは50文字以上で書いてください
    ・使用できる記号は「!!」と「!?」と「??」のみです。
    ・タイトル1:〇〇という形式で箇条書きで出力してください。
    ・過去のタイトルと被らないように気をつけてください'''

    response = claude_api.send_message(prompt, conversation_id)
    response_list = str(response.replace('\n','')).split(':')
    title_list = []
    # 考案するタイトル数によって変更必須
    for i in range(1,3):
        title = response_list[i]
        title = title.replace(' ','').replace(f'タイトル{i+1}','')
        title_list.append(title)
    
    return title_list



def headline(title):
    claude_api = Client('CLAUDE_PAGE_SESSION_DATA')
    conversation_id = "CLAUDE_PAGE_URL_ID"

    prompt = f'''「{title}」というブログ記事の見出しを下記の項目に注意して考えてください。
    ・見出し1:〇〇という形式で箇条書きで出力してください。
    '''
    response = claude_api.send_message(prompt, conversation_id)
    response_list = response.replace(' ','').replace('\n','').split('-')
    headline_list = []
    # 見出しがいくつあるかを判別しfor文を回す回数を指定する必要がある
    for i in range(1,int(response.count('-'))+1):
        headline = response_list[i]
        headline = headline.replace(f'見出し{i}:','')
        headline_list.append(headline)

    return headline_list

def content(title, headlines):
    claude_api = Client('CLAUDE_PAGE_SESSION_DATA')
    conversation_id = "CLAUDE_PAGE_URL_ID"
    ctx_dict = {}
    for i, headline in enumerate(headlines):
        print(f'文章を生成中...{i+1}/{len(headlines)}')
        prompt=f'「{title}」というタイトルの記事の「{headline}」という見出しの本文を1000文字以上で書いてください。本文:という形式で文章を作成してください。'
        response = claude_api.send_message(prompt, conversation_id)
        ctx = response.split('本文:')
        ctx = ctx[2]
        ctx_dict[headline] = ctx
    
    print('文章を生成中...まとめ')
    prompt=f'「{title}」というタイトルの記事のまとめを1000文字以内で書いてください。まとめ:という形式で文章を作成してください。'
    response = claude_api.send_message(prompt, conversation_id)
    ctx = response.split('まとめ:')
    ctx = ctx[2]
    ctx_dict['まとめ'] = ctx
    
    print('文章を生成中...リード文')
    prompt=f'「{title}」というタイトルの記事のリード文を1000文字以内で書いてください。リード文:という形式で文章を作成してください。'
    response = claude_api.send_message(prompt, conversation_id)
    ctx = response.split('リード文:')
    ctx = ctx[2]
    ctx_dict['リード文'] = ctx

    return ctx_dict

# CONTENT = '大学でおすすめのノートパソコン選び'
# CATEGORY = 'パソコン'

# for tit in title(CONTENT):
#     print(f'タイトル::{tit}')
#     print(f'見出しの生成開始')
#     headline_list = headline(tit)
#     print(f'見出しを{len(headline_list)}個生成しました')
#     ctx_dict = content(tit, headline_list)
#     md = ''
#     md += ctx_dict['リード文']+'\n\n'
#     for head, ctx in ctx_dict.items():
#         if head != 'リード文':
#             md += '##'+head+ctx+'\n\n'
#     html = markdown.markdown(md)
#     print('記事内容を出力します')
#     print(html)
#     print('\n\n================================')

