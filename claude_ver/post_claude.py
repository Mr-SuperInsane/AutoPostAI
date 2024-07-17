import requests, json, markdown
from create_claude import title, headline, content

CONTENT = 'パソコン'

# categories = wordpress_category_id

for i, tit in enumerate(title(CONTENT)):
    print(f'{i+1}記事目を作成中...')
    headline_list = headline(tit)
    ctx_dict = content(tit, headline_list)
    md = ''
    md += ctx_dict['リード文']+'\n\n'
    for head, ctx in ctx_dict.items():
        if head != 'リード文':
            md += '##'+head+ctx+'\n\n'
    html = markdown.markdown(md)

    status = 'draft'

    payload = {'title': tit ,'content' : html ,'status' : status, 'categories': 1}
    headers = {'content-type': "Application/json"}
    r = requests.post("https://YOUR-BLOG-URL/wp-json/wp/v2/posts", data=json.dumps(payload) , headers=headers, auth=('YOUR_WORDPRESS_USER_NAME', 'YOUR_WORDPRESS_API_TOKEN') )
    print('\n')
    if str(r) != '<Response [201]>':
        print('投稿に失敗しました')
        break

