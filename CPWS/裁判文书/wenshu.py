import json
import re
import random
import requests
import execjs

with open('js_decoder/encrypt.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
    ctx1 = execjs.compile(js1)
with open('js_decoder/ywtu.js', 'r', encoding="utf-8") as f:
    js2 = f.read()
    ctx2 = execjs.compile(js2)
with open('js_decoder/vl5x.js', 'r', encoding="utf-8") as fp:
    js = fp.read()
    ctx = execjs.compile(js)
with open('js_decoder/get_docid.js', encoding='utf-8') as f:
    js3 = f.read()
    ctx3 = execjs.compile(js3)

session = requests.session()


def get_vjkl5():
    url = 'http://wenshu.court.gov.cn/list/list/'
    headers = {
        'Host': 'wenshu.court.gov.cn',
        'Referer': 'http://wenshu.court.gov.cn/list/list/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    }
    res = session.get(url=url, headers=headers)
    vjkl5 = requests.utils.dict_from_cookiejar(res.cookies)['vjkl5']
    return vjkl5


def createGuid():
    return str(hex((int(((1 + random.random()) * 0x10000)) | 0)))[3:]


def getguid():
    """生成Guid"""
    return '{}{}-{}-{}{}-{}{}{}' \
        .format(
        createGuid(), createGuid(),
        createGuid(), createGuid(),
        createGuid(), createGuid(),
        createGuid(), createGuid()
    )


def get_vl5x(vjkl5):
    """生成Vl5x"""
    vl5x = ctx.call('getKey', vjkl5)
    return vl5x


def spider(vjkl5, guid, vl5x):
    """获取详情数据"""
    data = {
        "Param": "案件类型:刑事案件",
        "Index": "1",
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": vl5x,
        "number": "wens",
        "guid": guid
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Cookie': '_gscu_2116842793=52486773ryid8215; _gscbrs_2116842793=1; Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1566985895; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1566985982; vjkl5={}; _gscs_2116842793=66985895knyqtl11|pv:5'.format(
            vjkl5)
    }
    url = 'http://wenshu.court.gov.cn/List/ListContent'
    response = session.post(url=url, data=data, headers=headers)
    response.encoding = 'utf-8'
    return response.text


def get_docid(result):
    """
    :return: 返回文书ID列表
    """
    docid_list = []
    result = eval(json.loads(result))
    # 获取RunEval
    runeval = result[0]['RunEval']
    content = result[1:]
    for i in content:
        casewenshuid = i.get('文书ID', '')
        doc_id = decrypt_id(runeval, casewenshuid)
        docid_list.append(doc_id)
        return docid_list


def decrypt_id(RunEval, id):
    """
    docid解密
    """
    js = ctx3.call("GetJs", RunEval)
    js_objs = js.split(";;")
    js1 = js_objs[0] + ';'
    js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
    key = ctx3.call("EvalKey", js1, js2)
    key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
    docid = ctx3.call("DecryptDocID", key, id)
    return docid


def main():
    vjkl5 = get_vjkl5()
    guid = getguid()
    vl5x = get_vl5x(vjkl5)
    text = spider(vjkl5, guid, vl5x)
    id_list = get_docid(text)
    print(id_list)


if __name__ == '__main__':
    main()
