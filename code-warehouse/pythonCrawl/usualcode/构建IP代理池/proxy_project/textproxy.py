from test import Mysql_Test
from urllib.parse import urlencode
import requests,json,datetime,random,time,os,execjs,jsonpath
from fake_useragent import UserAgent
from requests.exceptions import ConnectionError
import pandas as pd
class testproxy(object):
    def __init__(self):
        self.mysqltest = Mysql_Test()
    def get_html(self,url):
        #从mysql数据库获取代理IP
        results = self.mysqltest.get_proxy()
        lis_proxy = []
        for result in results:
            proxy_ip = result[0]+'://'+result[1]+':'+result[2]
            proxies = {
                result[0]:proxy_ip
            }
            lis_proxy.append(proxies)
        try:
            # 打开解密的js获取密码
            with open(r'D:\Desktop\pythonCrawl\评级预测\js.js',encoding = 'utf-8',mode='r') as f:
                jsData = f.read()
                # 用execjs库获取js函数
                cipher = execjs.compile(jsData).call('getResCode')
            # 使用fakeuseragent库伪装请求头  
            ua = UserAgent()
            headers = {
                "Host":"webapi.cninfo.com.cn",
                "Connection":"keep-alive",
                "Content-Length":"0",
                "Accept":"*/*",
                "X-Requested-With":"XMLHttpRequest",
                "mcode":cipher,
                "User-Agent":ua.random,
                "Origin":"http://webapi.cninfo.com.cn",
                "Referer":"http://webapi.cninfo.com.cn/",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Cookie":"Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1609811200; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b=1609811200",
                    }
            response = requests.post(url,headers=headers,proxies=random.choice(lis_proxy),timeout=10).text
            return response
        except Exception:
            print('代理IP请求失败等待再次请求..')
            get_html(url)
    def save_data(self,page):
        # #判断如果请求失败，再次请求
        max_repeat= 0
        while max_repeat<2:
            try:
                # 拼接url传给get_html，返回请求信息
                url = f"http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1089?tdate={page}"
                # 象征性停1s再请求
                time.sleep(1)
                html = testproxy().get_html(url)
                # 将获取到的数据转化为json数据
                data = json.loads(html)
                # 从json数据中提取需要的关键字
                new_data = data['records']
                data_lis = []
                # 循环遍历json数据提取每个指标
                for nd in new_data:
                    SECCODE = nd['SECCODE'] # 证券代码
                    SECNAME = nd['SECNAME'] # 证券简称
                    DECLAREDATE = nd['DECLAREDATE'] # 日期
                    F002V = nd['F002V'] # 研究机构简称
                    F003V = nd['F003V'] # 研究员名称
                    F004V = nd['F004V'] # 投资评级
                    F006V = nd['F006V'] # 是否首次评级
                    F007V = nd['F007V'] # 评级变化
                    F008V = nd['F008V'] # 前一次投资评级
                    F009N = nd['F009N'] # 目标价格(下限)
                    F010N = nd['F010N'] # 目标价格(上限)
                    lis = [SECCODE,SECNAME,DECLAREDATE,F002V,F003V,F004V,F006V,F007V,F008V,F009N,F010N]
                    # 将获取的字段追加到data_lis列表中
                    data_lis.append(lis)
                # 使用pandas保存所获取消息
                df = pd.DataFrame(data_lis,columns=['证券代码','证券简称','日期','研究机构简称','研究员名称','投资评级','是否首次评级','评级变化','前一次投资评级','目标价格(下限)','目标价格(上限)'])
                #判断是否有标题，无则追加
                if not os.path.isfile("test.csv"):
                    df.to_csv('test.csv',index=False,mode='a',encoding='utf_8_sig',index_label=False)
                else:
                    df.to_csv('test.csv',index=False,mode='a',encoding='utf_8_sig',index_label=False,header=0)
                print(page,"保存成功!")
                break
            except Exception:
                print(f"{page} 未获取到数据,等待重新尝试！")
                # 等待五秒后再次尝试
                time.sleep(5)
            max_repeat+=1
if __name__ == '__main__':
    #循环输出日期
    start=input('请输入开始时间(yyyy-mm-dd)：')
    end=input('请输入截至时间(yyyy-mm-dd)：')
    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
    while datestart<dateend:
        datestart+=datetime.timedelta(days=1)
        dateAll = datestart.strftime('%Y-%m-%d')
        testproxy().save_data(dateAll)