import re

import requests
from lxml import etree

from GM.DZDP.font import ParseFontClass


def spider(data_content):
    """
    解析函数
    :param data_content:  商铺链接信息
    :return: item 店铺详情
    """
    font_list = []
    num_list = []
    item = dict()
    res = requests.get(**data_content)
    tree = etree.HTML(res.text)
    # css_url svg的css链接地址
    css_url = 'https:' + ''.join(
        [css_url for css_url in tree.xpath('//link[@rel="stylesheet"]/@href') if 'svgtextcss' in css_url])
    # 传入页面中包含字体链接的 css 网址
    pf = ParseFontClass(css_url)
    # 获取商铺地址信息
    address = ''.join(re.findall(
        r'<span class="item" itemprop="street-address" id="address">(.*?)<div class="addressIcon"></div>',
        res.text)).replace('<e class="address">', '+').replace('<d class="num">', '+').replace('</e>', '+').replace(
        '</d>', '+').replace('</span>', '')
    address_list = [x for x in address.split('+') if x != '']
    for ttf in address_list:
        # 如果包含 & 就是字体
        if '&' in ttf:
            # 如果为False 就是数字
            if pf.parse_ttf(ttf):
                font_list.append(pf.parse_ttf(ttf))
            else:
                font_list.append(pf.parse_num(ttf))

        else:
            font_list.append(ttf)
    item['地址'] = ''.join(font_list).strip()

    phone = ''.join(
        re.findall(r'<span class="info-name">电话：</span>(.*?)</p> <div class="promosearch-wrapper">', res.text)).replace(
        '<d class="num">', '+').replace('</d>', '+')
    phone_list = [x for x in phone.split('+') if x != '']
    for _ in phone_list:
        # 如果包含 & 就是数字
        if '&' in _:
            # 如果为False就是空白字符
            if pf.parse_num(_) != False:
                num_list.append(pf.parse_num(_))
            else:
                num_list.append(' ')
        else:
            num_list.append(_)

    item['电话'] = ''.join(num_list).strip()
    return item