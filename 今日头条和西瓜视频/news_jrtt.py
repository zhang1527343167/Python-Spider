import requests
import json
import time
import random
import re
import base64
from zlib import crc32

s = requests.session()


def video_content(news_url, headers, item):
    """获取西瓜视频数据"""
    res = s.get(url=news_url, headers=headers)
    vid = re.findall(r'"vid":"(.*?)",', res.text)[0]
    r = str(random.random())[2:]
    url = "/video/urls/v/l/toutiao/mp4/{}?r={}".format(vid, r)
    _s = crc32(url.encode())
    url = "https://ib.365yg.com{}&s={}".format(url, _s)
    resq = s.get(url, headers=headers)
    j_resp = resq.json()
    video_url = j_resp['data']['video_list']['video_1']['main_url']
    video_url = base64.b64decode(video_url).decode()
    item['video_url'] = video_url
    print(item)


def content(content_list, headers):
    """获取新闻数据"""
    for _ in content_list:
        item = dict()
        news_url = _['share_info']['share_url']
        item['title'] = _['share_info']['title']
        item['url'] = news_url
        item['time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(_['behot_time']))
        text = s.get(url=news_url, headers=headers).text
        content = re.findall(r"content: '(.*?)'\.slice|<article>(.*?)</article>", text.replace('\n', ''))
        # 如果为[]就是视频数据
        if content != []:
            item['content'] = ''.join(content[0])
            print(item)
        else:
            video_content(news_url, headers, item)


def spider(url, headers):
    """获取新闻url列表"""
    resp = s.get(url=url, headers=headers)
    # 0,1是置顶数据过滤掉
    obj = json.loads(resp.text)['data'][2:]
    content_list = [json.loads(i['content']) for i in obj]
    return content_list


def main():
    # 今日头条app推荐板块接口
    url = 'http://ic.snssdk.com/api/news/feed/v88/?list_count=16&refer=1&count=20'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    }
    content_list = spider(url, headers)
    content(content_list, headers)


if __name__ == '__main__':
    main()
