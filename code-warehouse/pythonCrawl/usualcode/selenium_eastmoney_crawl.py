from selenium import webdriver
import time,os
from time import sleep
import pandas as pd
driver = webdriver.Chrome('D:\chrome\chromedriver.exe')
driver.get('http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1')
i = 1
while i<=10:
    code = driver.find_elements_by_xpath('//*[@id="oTable"]/tbody/tr')
    lis_data = []
    for cd in code:
        xh = cd.find_element_by_xpath('./td[@class="xh"]').text
        bzdm = cd.find_element_by_xpath('./td[@class="bzdm"]').text
        tol = cd.find_element_by_xpath('./td[@class="tol"]/nobr').text       
        dwjz1 = cd.find_element_by_xpath('./td[6]').text
        ljjz1 = cd.find_element_by_xpath('./td[7]').text
        dwjz2 = cd.find_element_by_xpath('./td[8]').text
        ljjz2 = cd.find_element_by_xpath('./td[9]').text
        rzzl1 = cd.find_element_by_xpath('./td[10]').text
        rzzl2 = cd.find_element_by_xpath('./td[11]').text
        sgzt = cd.find_element_by_xpath('./td[12]').text
        xhzt = cd.find_element_by_xpath('./td[13]').text
        sxf = cd.find_element_by_xpath('./td[14]/div/div[@class="rate_f"]').text
        lis = [bzdm,tol,dwjz1,ljjz1,dwjz2,ljjz2,rzzl1,rzzl2,sgzt,xhzt,sxf]
        lis_data.append(lis)
        print("序号:",xh,lis)
    df = pd.DataFrame(lis_data,columns=['基金代码','基金简称','单位净值2021-01-04','累计净值2021-01-04',
                                        '单位净值2020-12-31','累计净值2020-12-31','日增长值2021-01-04','日增长率2020-12-31',
                                        '申购状态','赎回状态','手续费'])
    if not os.path.isfile('text.csv'):
        df.to_csv('test.csv',mode='a',encoding='utf_8_sig',index=False)
    else:
        df.to_csv('test.csv',mode='a',encoding='utf_8_sig',index=False,header=0)
    driver.find_element_by_xpath('//*[@id="pager"]/span[8]').click()
    driver.close
    i+=1
    time.sleep(3)