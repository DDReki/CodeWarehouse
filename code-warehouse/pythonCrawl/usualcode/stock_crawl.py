from lxml import etree
import requests,re,os,time,random,json
from fake_useragent import UserAgent
import jsonpath
import pandas as pd
ua =UserAgent()
# proxy = ['http://41.229.253.214:8080',
#  'http://103.57.143.246:61148',
#  'http://103.57.143.246:61148'
#         ]
# proxy_random = random.choice(proxy)
# proxy_ip = {'http':proxy_random}
head = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip,deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Cookie":"Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1609138169;historystock=000001;spversion=20130314;Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1609138215;v=Aw1xXVfjbgW-2sopOLB4yW_8HCKE6k2EyxalnU-SSUMTECNUFzpRjFtutWrc",
    "Host":"d.10jqka.com.cn",
    "If-Modified-Since":"Mon, 28 Dec 2020 07:21:36 GMT",
    "Referer":"http://m.10jqka.com.cn/",
    "User-Agent":ua.random,
}
url = 'https://hq.gucheng.com/gpdmylb.html'
response = requests.get(url)
html_str = response.content.decode('utf-8')
html = etree.HTML(html_str)
stock_code = html.xpath('//*[@id="stock_index_right"]/div[3]/section/a/text()')
for sc in stock_code:
    try:
        a1 = re.findall(r'(\(.*?\))',sc)
        a2 = ', '.join(a1)
        scode = re.sub('[^0-9,]','',a2)
        scode_url = 'http://d.10jqka.com.cn/v6/realhead/hs_{}/last.js'.format(scode)
        print(scode_url)
        res = requests.get(scode_url,headers = head)
        data = res.content.decode('utf-8')
        #去掉获取到的数据前面无用的，不然无法将json格式数据转换为字典
        comment = 'quotebridge_v6_realhead_hs_{}_last'.format(scode)
        comments =data.lstrip(''+comment+'(').rstrip(');')
        content = json.loads(comments)
        scodeinfo = jsonpath.jsonpath(content,"$..items")
    except:
        print('数据错误')
    print(scodeinfo)
    infos = []
    for si in scodeinfo:
        today = si['7']
        highest = si['8']
        minimum = si['9']
        info = [today,highest,minimum]
        infos.append(info)
    df = pd.DataFrame(infos,columns=['今日开','最高','最低'])
    if not os.path.isfile('socde.csv'):
        df.to_csv('socde.csv',index=False,mode='a',encoding='utf_8_sig')
    else:
        df.to_csv('socde.csv',index=False,mode='a',encoding='utf_8_sig',header=0)