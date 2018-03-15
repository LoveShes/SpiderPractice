import requests # 网络请求模块
import re # 匹配数据模块
import time # 用到其中的time.sleep，

for n in range(1,100):
    list_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_' + str(n) + '.html'
    html_1 = requests.get(list_url)
    html_1.encoding = 'gb2312'
    # print(html_1.status_code)
    detail_list = re.findall('<a href="(.*?)" class="ulink">', html_1.text)
    for info in detail_list:
        movie_url = 'http://www.dytt8.net' + info
        html_2 = requests.get(movie_url)
        html_2.encoding = 'gb2312'
        info = re.findall('<a href="(.*?)">.*?</a></td>', html_2.text)
        with open('.\movies.txt', 'a', encoding='utf-8') as f:
            f.write(info[0] + '\n')
    time.sleep(2)
