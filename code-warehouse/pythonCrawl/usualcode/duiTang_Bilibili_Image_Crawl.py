#堆糖
import urllib.parse
from fake_useragent import UserAgent
import requests,os,json,random
import jsonpath
ua = UserAgent()
headers = {
    'Cookie': 'sessionid=e32aeda1-2de4-4c7c-bd74-2e8d892b7066; __guid=173196965.1861602199333012700.1608781689898.0266; Hm_lvt_d8276dcc8bdfef6bb9d5bc9e3bcfcaf4=1608781691; monitor_count=5; js=1; Hm_lpvt_d8276dcc8bdfef6bb9d5bc9e3bcfcaf4=1608781869',
    'Host': 'www.duitang.com',
    'Origin': 'https://www.duitang.com',
    'Referer': 'https://www.duitang.com/',
    'User-Agent':ua.random
}
base_url = "https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}"
kw = input("请输入需要爬取的图片类型:")
kw = urllib.parse.quote(kw)
n = int(input('请输入需要爬取的页数(24为一页):'))
num = 0
for i in range(0,n,24):
    url = base_url.format(kw,i)
    res = requests.get(url,headers=headers).text
    data = json.loads(res)
    photo = jsonpath.jsonpath(data,"$..path")
    print(photo)
    for j in photo:
        with open(r'photo\{}.jpg'.format(num),'wb') as f:
            f.write(requests.get(j).content)
        num+=1

#bilibili
import urllib.parse
from fake_useragent import UserAgent
import requests,os,json,random
import jsonpath
from hyper.contrib import HTTP20Adapter
ua = UserAgent()
headers = {
    'authority':'api.vc.bilibili.com',
    'method':'GET',
    'accept':'application/json,text/plain,*/*',
    'accept-encoding':'gzip,deflate,br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':"l=v;_uuid=BF7B5522-1144-31E1-F57D-6D3B683E4A8809807infoc;buvid3=A83F8F3B-EA1D-4DC1-8AB6-CC7D41F42F1758478infoc;LIVE_BUVID=AUTO8916069005486126;CURRENT_FNVAL=80;blackside_state=1;DedeUserID=2848435;DedeUserID__ckMd5=182f45b1932183ba;SESSDATA=a9fec077%2C1623659995%2C3c8d8*c1;bili_jct=6a459101498891c1e12533ac726345a0;rpdid=|(JYYJk|~)uu0J'uY|)lJluYu;bsource=search_baidu;PVID=3",
    'origin':'//h.bilibili.com',
    'referer':'//h.bilibili.com/eden/draw_area',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
    'user-agent':ua.random,
}
base_url = "https://api.vc.bilibili.com/link_draw/v2/Doc/list?category=all&type=hot&page_num={}&page_size=20"
n = int(input('请输入需要爬取的页数:'))
num = 0
try:
    for i in range(0,n):
        time.sleep(1)
        url = base_url.format(i)
        res = requests.get(url,headers=headers).text
        data = json.loads(res)
        photo = jsonpath.jsonpath(data,"$..img_src")
        for j in photo:
            with open(r'bilibiliimages\{}.jpg'.format(num),'wb') as f:
                f.write(requests.get(j).content)
                print('保存成功')
            num+=1
except:
    print("保存失败")