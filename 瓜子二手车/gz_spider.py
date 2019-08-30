import execjs
import re
import requests

# 获取 js
with open('gz.js', 'r', encoding="utf-8") as fp:
    js = fp.read()
    ctx = execjs.compile(js)


def spider(url, headers):
    """解析函数"""
    session = requests.session()
    # 第一次访问 得到 js 代码
    response = session.get(url=url, headers=headers)
    # 获取 anti() 所需参数
    key_list = re.findall(r"var value=anti\('(.*?)'\)", response.text)[0].split(',')
    # 获取 string, key
    string, key = key_list[0].replace("'", ''), key_list[1].replace("'", '')
    parse = ctx.call('getKey', string, key)
    name = 'antipas'
    # 获得 antipas
    antipas = ctx.call('xredirect', name, parse, '')
    headers['Cookie'] = antipas
    headers['Referer'] = 'https://www.guazi.com/cd/3f78c6cf1f554592x.htm'

    # 第二次访问成功返回数据
    res = session.get(url=url, headers=headers)
    return res.text


def main():
    """ 获取瓜子二手车  Cookie antipas值
    """
    url = 'https://www.guazi.com/cd/3f78c6cf1f554592x.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    text = spider(url, headers)
    print(text)


if __name__ == '__main__':
    main()
