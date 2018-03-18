import requests
import json
import time
import os

def image_spider(image_url, date, index, user_name, image_count):
    file_type = image_url.split('.')[-1]
    file_path = 'weibo_spider/image/'  
    image_path = 'weibo_spider/image/{0}/'.format(user_name)
    image_name = image_path + date + '_{0:02}.{1}'.format(index,file_type)
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    if not os.path.exists(image_path):
        os.mkdir(image_path)
        print("目录创建成功！")
        
    if (image_url):
        image = requests.get(image_url, stream=True) 
        if not os.path.exists(image_name): 
            with open(image_name, 'wb+') as f:
                f.write(image.content)
                print('\r成功下载第{0:08}张图片'.format(image_count), end='')
        else:
            print('\r第{0:08}张图片已经存在'.format(image_count), end='')

def html_spider(ID, pages=500):
    image_count = 0
    for n in range(1,pages+1):
        url = 'https://m.weibo.cn/api/container/getIndex?page={0}&type=uid&value={1}&containerid=107603{1}'.format(n,ID)
        html = requests.get(url)
        html_json = json.loads(html.text)
        cards = html_json['data']['cards']
        if cards == []:
            print('\n\n该用户全部图片下载完毕！')
            break
        for card in cards:
            if ('mblog' in card):
                date = card['mblog']['created_at']
                user_name = card['mblog']['user']['screen_name']
                if len(date) < 10:
                    date = '2018-' + date
                if ('pics' in card['mblog']):
                    images = card['mblog']['pics']
                    for index, image in enumerate(images):
                        image_url = image['large']['url']
                        image_count += 1
                        image_spider(image_url, date, index+1, user_name, image_count)
    time.sleep(2)   # 每爬取1页就暂停2秒 

def main():
    print("请输入想要爬取用户的主页地址，每个用户以换行符结束，输入q表示输入结束：")
    users_list = []  
    while True:  
        users_url = input()      
        if users_url == 'q' :
            print('输入完毕！')
            break
        else:
            users_list.append(users_url)    
    for n, user_url in enumerate(users_list):
        user_ID = user_url[-10:]
        print('\n正在爬取第{0}个用户的微博图片...\n'.format(n+1))
        html_spider(user_ID) 
    print('\n全部用户爬取完毕！程序已退出运行')


if __name__ == '__main__':
    main()

