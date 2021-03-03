import requests,time
from lxml import etree

from MysqlClient import MysqlClient
from VerifyProxy import VerifyProxy

class CrawlProxy(object):
    def __init__(self):
        self.mysql = MysqlClient()
        self.verify = VerifyProxy()
    def get_free_proxy(self):
        n = int(input("请输入需爬取的页数："))
        for i in range(0,n):
            url = f'https://ip.jiangxianli.com/?page={i}'
            response = requests.get(url).text
            html = etree.HTML(response)
            content = html.xpath('//*[@class="layui-table"]/tbody/tr')
            time.sleep(1)
            for j in content:
                scheme = j.xpath('./td[4]/text()')[0].lower()
                ip = j.xpath('./td[1]/text()')[0]
                port = j.xpath('./td[2]/text()')[0]
                Anonymous_degrees = j.xpath('./td[3]/text()')[0]
                verify_result = self.verify.verify_proxy(scheme,ip,port,Anonymous_degrees)
                if verify_result['status'] == '1':
                    proxy = {
                        "scheme":scheme,
                        "ip":ip,
                        "port":port,
                        "Anonymous_degrees":Anonymous_degrees,
                        "status":verify_result["status"],
                        "response_time":verify_result["response_time"]
                    }
                    self.mysql.add_proxy(proxy)
                    print(f"代理{ip}链接测试已通过,已保存Mysql")
                else:
                    print(f'代理{ip}链接测试未通过')
if __name__ == "__main__":
    CrawlProxy().get_free_proxy()