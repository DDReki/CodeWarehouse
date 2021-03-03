import requests
from MysqlClient import MysqlClient
class VerifyProxy(object):
    def __init__(self):
        self.mysql = MysqlClient()
    def verify_proxy(self,scheme,ip,port,Anonymous_degrees):
        proxies = {
            scheme : scheme + '://' + ip + ':' + port
        }
        response_time = 0
        status = '0'
        try:
            response = requests.get(scheme + '://httpbin.org/ip',proxies=proxies,timeout=5)
            if response.status_code==200:
                response_time = round(response.elapsed.total_seconds()*1000)
                status = '1'
                print(f'{proxies}能使用!')
            else:
                response_time = 0
                status = '0'
                print(f'{proxies}不能使用!')
        except:
            pass 
        return {"response_time":response_time,"status":status}
    def verify_all(self):
        results = self.mysql.find_all()
        for result in results:
            res = self.verify_proxy(result[1],result[2],result[3],result[4])
            proxy = {
                "id":result[0],
                "scheme":result[1],
                "ip":result[2],
                "port":result[3],
                "Anonymous_degrees":result[4],
                "status":res["status"],
                "response_time":res["response_time"]
            }
        self.mysql.update_proxy(proxy)
        print('检查完毕..')
if __name__=="__main__":
    VerifyProxy().verify_all()