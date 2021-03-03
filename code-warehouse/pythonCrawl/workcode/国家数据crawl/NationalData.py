import requests,json,jsonpath,time,os
import numpy as np
import pandas as pd
from lxml import etree
requests.packages.urllib3.disable_warnings() #移除警告
url = 'https://data.stats.gov.cn/easyquery.htm?'
header = {
    "Accept":"application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Connection":"keep-alive",
    "Cookie":"JSESSIONID=QWPf1Z1fMqiYKYO4VJ85vUi3eUqxGBUO4biKAAtTxCmNoUe3TGL0!-275752630; u=2; _trs_uv=kjnoad3n_6_a5pk",
    "Host":"data.stats.gov.cn",
    "Referer":"https://data.stats.gov.cn/easyquery.htm?cn=E0103",
    "Sec-Fetch-Dest":"empty",
    "Sec-Fetch-Mode":"cors",
    "Sec-Fetch-Site":"same-origin",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
}
provinces = ['110000','120000','130000','140000','150000','210000','220000','230000','310000','320000','330000','340000','350000','360000','370000','410000','420000','430000','440000','450000','460000','500000','510000','520000','530000','540000','610000','620000','630000','640000','650000']
indicators = ['A0101','A010201','A010202','A010203','A010301','A010302','A0201','A0202','A0203','A0204','A0205','A0301','A0302','A0303','A030801','A030802','A030803','A030804','A030805','A030806','A030807','A030808','A0401','A0402','A0403','A0404','A0405','A0406','A0407','A0408','A0409','A040A','A040B','A040C','A0501','A0502','A0503','A0504','A0505','A0506','A0507','A0508','A0509','A050A','A050B','A050C','A050D','A050E','A050F','A050G','A050H','A050I','A050J','A051C','A051D','A051E','A051F','A051G','A051H','A051I','A051J','A051K','A051L','A051M','A051N','A051O','A051P','A051Q','A0601','A0602','A0603','A0604','A0701','A0702','A0703','A0704','A0705','A0706','A0707','A0801','A0802','A0901','A090A','A0902','A0903','A0904','A0905','A0906','A0907','A0908','A0909','A0A00','A0A01','A0A02','A0A03','A0A04','A0A05','A0A06','A0A09','A0A0A','A0B01','A0B02','A0B03','A0B04','A0B05','A0B06','A0B07','A0B08','A0B09','A0B0A','A0C01','A0C02','A0C03','A0C04','A0C05','A0C06','A0C08','A0C0A','A0C0B','A0C0C','A0C0D','A0C0G','A0C0H','A0C0I','A0C0J','A0C0K','A0C0L','A0C0M','A0C0N','A0C0O','A0C0P','A0D01','A0D02','A0D03','A0D05','A0D06','A0D0G','A0D0H','A0D0I','A0D0J','A0D0K','A0D0L','A0D0M','A0D0N','A0D0O','A0D0P','A0D0Q','A0D0R','A0D0S','A0D0T','A0D0U','A0D0V','A0D0W','A0D0X','A0D0Y','A0D0Z','A0D10','A0D11','A0D12','A0D13','A0D14','A0D15','A0D17','A0D18','A0E01','A0E02','A0E03','A0E04','A0E05','A0E0B','A0F01','A0F02','A0F03','A0F04','A0F05','A0F06','A0F07','A0F08','A0F09','A0F0A','A0F0B','A0F0C','A0F0D','A0F0E','A0F0F','A0F0G','A0F0H','A0F0I','A0F0J','A0F0K','A0F0L','A0F0M','A0F0N','A0F0O','A0F0P','A0F0Q','A0F0R','A0F0S','A0F0T','A0F0U','A0F0V','A0F0W','A0F0X','A0F0Y','A0F0Z','A0G01','A0G02','A0G03','A0G04','A0G05','A0G06','A0G07','A0G08','A0G09','A0G0A','A0G0B','A0G0C','A0G0D','A0G0E','A0G0F','A0G0G','A0G0H','A0G0I','A0G0J','A0G0K','A0H','A0I01','A0I02','A0I03','A0I04','A0I05','A0I06','A0I07','A0I08','A0I09','A0I0A','A0J01','A0J02','A0J03','A0J04','A0J05','A0J06','A0J07','A0J08','A0J09','A0K01','A0K02','A0L01','A0M01','A0M02','A0M03','A0M04','A0M05','A0M06','A0M07','A0M08','A0M09','A0M0A','A0M0B','A0M0C','A0M0D','A0N01','A0N02','A0N03','A0N04','A0N05','A0N06','A0N07','A0N08','A0N09','A0N0A','A0N0B','A0N0C','A0N0D','A0O01','A0O02','A0O03','A0O04','A0O05','A0O06','A0O07','A0O08','A0O09','A0O0A','A0O0B','A0O0C','A0P01','A0P02','A0P03','A0P04','A0P05','A0P06','A0P07','A0P08','A0P09','A0P0A','A0P0B','A0P0C','A0Q01','A0Q02','A0Q03','A0Q04','A0Q05','A0Q06','A0Q07','A0Q08','A0Q09','A0Q0A','A0Q0B','A0Q0C','A0Q0D','A0Q0E','A0Q0F','A0Q0G','A0R01','A0R02','A0S01','A0S02','A0S03','A0S04','A0S05','A0S06','A0S07','A0S08','A0S0A','A0S0B']
for i in provinces:
        time.sleep(1)
        for j in indicators:
            try:
                time.sleep(1)
                params={
                    'm':'QueryData',
                    'dbcode':'fsnd',
                    'rowcode':'zb',
                    'colcode':'sj',
                    'wds':'[{"wdcode":"reg","valuecode":' + '"' + str(i) +'"' +'}]',
                    'dfwds':'[{"wdcode":"zb","valuecode":' + '"' + str(j) +'"' +'}]',
                    'k1':round(time.time() * 1000),
                    'h':'1'
                }
                response = requests.get(url,verify=False,headers = header,params = params).text
                jsondata = json.loads(response)
                #获取指标名
                lis1 = jsonpath.jsonpath(jsondata,'$.returndata.wdnodes[0].nodes')
                target = jsonpath.jsonpath(lis1,'$..cname')
                unit = jsonpath.jsonpath(lis1,'$..unit')
                unit_new = [':'+ __ for __ in unit]
                targets = [i+j for i,j in zip(target,unit_new)]
                # 获取日期
                lis2 = jsonpath.jsonpath(jsondata,'$.returndata.wdnodes[2].nodes')
                years = jsonpath.jsonpath(lis2,'$..cname')
                #获取省份
                lis3 = jsonpath.jsonpath(jsondata,'$.returndata.wdnodes[1].nodes')
                province = jsonpath.jsonpath(lis3,'$..cname')
                #获取数据
                lis4 = jsonpath.jsonpath(jsondata,'$..strdata]')
                #按指标和日期长度分成几行几列的数据
                array = np.array(lis4).reshape(len(target),len(years))
                df = pd.DataFrame(array,columns=years,index=pd.MultiIndex.from_product([targets,province]))
                if not os.path.isfile('gjdata.csv'):
                    df.to_csv('gjdata.csv',encoding='utf_8_sig',mode='a')
                else:
                    df.to_csv('gjdata.csv',encoding='utf_8_sig',mode='a',header = 0)
                print(f'{i},指标:{j}保存成功..')
            except:
                print(f'{i},指标:{j}保存失败,继续下一个..')                