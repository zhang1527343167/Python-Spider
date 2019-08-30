import json
import os
import re

import redis
import requests
from fontTools.ttLib import TTFont

from GM.大众点评.setting import *


class ParseFontClass:
    def __init__(self, css_url):
        """
        redis 默认链接本机
        REDIS_HOST redis连接参数
        """
        self.ttf = None
        self.num = None
        pool = redis.ConnectionPool(**REDIS_HOST)
        self.r = redis.Redis(connection_pool=pool)

        self.css_url = css_url
        self.remove()
        self.start()

    def parse_num(self, code):
        """数字对应库"""
        clean_code = code.replace(';', '')[-4:]  # 只提取匹配区域
        result_list = self.r.hmget(HASH_NUM, self.num)  # 取出对应字库表

        for result in result_list:
            json_data = json.loads(result)
            if 'uni' + clean_code in json_data:
                return json_data['uni' + clean_code]
        return False

    def parse_ttf(self, code):
        """字体对应库"""
        clean_code = code.replace(';', '')[-4:]  # 只提取匹配区域
        result_list = self.r.hmget(HASH_TABLE, self.ttf)  # 取出对应字库表
        for result in result_list:
            json_data = json.loads(result)
            if 'uni' + clean_code in json_data:
                return json_data['uni' + clean_code]
        return False

    def font_add_hash(self, name, json_data):
        """新增 汉字hash
        """
        self.r.hset(HASH_TABLE, name, json_data)

    def num_add_hash(self, name, json_data):
        """新增 数字hash
        """
        self.r.hset(HASH_NUM, name, json_data)

    def ttf_check_hash(self, name):
        """判断 hash key 是否存在
        """
        return self.r.hexists(HASH_TABLE, name)

    def num_check_hash(self, name):
        """判断 hash key 是否存在
        """
        return self.r.hexists(HASH_NUM, name)

    def get_font(self, ttf_list):
        for index, name in enumerate(self.ttf):
            if self.ttf_check_hash(name):
                # 已存在无需安装
                continue
            # 安装汉字字体
            with open('woff/' + name + '.woff', 'wb+') as f:
                f.write(requests.get('http://' + ttf_list[index]).content)  # 下载文本
                font = TTFont('woff/' + name + '.woff')
                uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()  # 对应关系拼接
                json_data = json.dumps(dict(zip(uni_list, FONT_LIST)), ensure_ascii=False)
                self.font_add_hash(name, json_data)

    def get_num(self, ttf_list):
        for index, name in enumerate(self.num):
            if self.num_check_hash(name):
                # 已存在无需安装
                continue
            # 安装数字字体
            with open('woff/' + name + '.woff', 'wb+') as f:
                f.write(requests.get('http://' + ttf_list[index + 1]).content)  # 下载文本
                font = TTFont('woff/' + name + '.woff')
                uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
                json_data = json.dumps(dict(zip(uni_list, FONT_LIST)), ensure_ascii=False)  # 对应关系拼接
                self.num_add_hash(name, json_data)

    def get_ttf(self, css_url):
        """获取字体链接
        """
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        result = requests.get(css_url, headers=headers)
        if result.status_code == 200:
            self.install_ttf(self.get_ttf_urls(result.text))
        else:
            return None

    def install_ttf(self, ttf_list):
        """安装字体
        """
        # self.ttf是汉字库名 self.num是数字库名
        name_list = [ttf[ttf.rfind('/') + 1: -5] for ttf in ttf_list]  # 提取相应的字库名
        self.ttf = [name_list[0]]
        self.num = [name_list[1]]
        self.get_font(ttf_list)
        self.get_num(ttf_list)

    @staticmethod
    def get_ttf_urls(text):
        """提取字体和数字链接
        """
        # 汉字
        font_text = re.findall(r"""address";src:url(.*?).address{font-family: 'PingFangSC-Regular-address';}""", text)[
            0]
        # 数字
        num_text = re.findall(r"""num";src:url(.*?) .num{font-family: 'PingFangSC-Regular-num';}""", text)[0]
        font_urls = [x for x in re.findall(r'url\("//(.*?)"\)', font_text) if x not in [] and '.woff' in x]
        num_urls = [x for x in re.findall(r'url\("//(.*?)"\)', num_text) if x not in [] and '.woff' in x]
        return font_urls + num_urls

    def remove(self):
        """删除旧文件 节省资源占用"""
        path_list = os.listdir('.\woff')
        # 如果不为空[]
        if path_list:
            for path in path_list:
                os.remove('woff/' + path)  # 添加完成后删掉，节省资源占用

    def start(self):
        self.get_ttf(self.css_url)
