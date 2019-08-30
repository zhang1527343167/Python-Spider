import execjs


def main():
    """ 获取瓜子二手车  Cookie antipas值
    """
    # 获取 js
    with open('gz.js', 'r', encoding="utf-8") as fp:
        js = fp.read()
        ctx = execjs.compile(js)

    # 调用 js 生成 cookie antipas
    parse = ctx.call('anti')
    print('antipas : %s' % len(parse))


if __name__ == '__main__':
    main()
