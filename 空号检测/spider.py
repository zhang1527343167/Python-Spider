import execjs

with open('string.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
    ctx1 = execjs.compile(js1)

with open('code.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
    ctx2 = execjs.compile(js1)

a = '15012819681'
c = '043AOQGK6ykklyZA'
h = '043AOQGK6ykklyZA'
string = ctx1.call("GetKey", a, c, h)
code = ctx2.call("GetCode", string)
print(code)
