# -*- coding: utf-8 -*-
# __author__ = "zgm"  1527343167@qq.com
# Date: 2019-08-30
from GM.大众点评.spider import spider


def main():
    """ data_content 需要抓取的 url 和 user_agent
    """
    data_content = {
        'url': 'http://www.dianping.com/shop/1879744',
        'headers': {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36                   (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
    }
    item = spider(data_content)
    print(item)


if __name__ == '__main__':
    main()
