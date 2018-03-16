import requests
import re
import time
import json
import os
from bs4 import BeautifulSoup

def image_spider(weiboID):
    url = 'https://m.weibo.cn/status/' + weiboID
    html = requests.get(url)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html.parser')
    imageID = soup.body.script.string.split('"pic_ids": [')[1].split('],')[0]
    image_urlist = imageID.split(',')
    user_path = 'weibo_spider/image/'
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    for image_url in image_urlist:
        image_url = image_url.strip() 
        image_url = image_url.replace('\n', '')
        image_url = image_url.replace('"', '')
        if (image_url):
            url = 'https://wx4.sinaimg.cn/large/' + image_url + '.jpg'
            image = requests.get(url, stream=True)  
            with open(user_path + '{0}.jpg'.format(image_url), 'wb+') as f:
                f.write(image.content)


def main_spider(ID, pages):
    for n in range(1,pages+1):
        url = 'https://m.weibo.cn/api/container/getIndex?page={0}&type=uid&value={1}&containerid=107603{1}'.format(n,ID)
        html = requests.get(url)
        html_json = json.loads(html.text)
        cards = html_json['data']['cards']
        for card in cards:
            if ('mblog' in card.keys()):
                weiboID = card['mblog']['id']
                image_spider(weiboID)


main_spider(2255058517,1)
