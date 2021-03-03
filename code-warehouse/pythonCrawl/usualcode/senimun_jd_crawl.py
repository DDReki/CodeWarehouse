from selenium import webdriver
import time,os
from lxml import etree
import pandas as pd
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('D:\chrome\chromedriver.exe',options=chrome_options)
# driver = webdriver.Chrome('D:\chrome\chromedriver.exe')
driver.implicitly_wait(10)
driver.set_window_size(1280,800)
def get_page(page,content,brand):
    print(f'正在获取{page}页数据..')
    try:
        url = f'https://search.jd.com/search?keyword={content}&ev=exbrand_{brand}'
        driver.get(url)
        js = '''
               timer = setInterval(function(){
               var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
               var ispeed=Math.floor(document.body.scrollHeight / 100);
               if(scrollTop > document.body.scrollHeight * 90 / 100){
                   clearInterval(timer);
               }
               console.log('scrollTop:'+scrollTop)
               console.log('scrollHeight:'+document.body.scrollHeight)
               window.scrollTo(0, scrollTop+ispeed)
            }, 20)
            '''
        driver.execute_script(js)
        time.sleep(2.5)
        if page>=1:
            input_page = driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[2]/input')
            sure_button =  driver.find_element_by_xpath('//*[@id="J_bottomPage"]/span[2]/a')
            input_page.clear()
            input_page.send_keys(page)
            time.sleep(3)
            sure_button.click()
        else:
            print('页码错误..')
        main()
    except:
        print('请求失败..')
#         get_page(page)
def main():
    pagesource = driver.page_source
    html = etree.HTML(pagesource)
    content = html.xpath('//*[@class="gl-i-wrap"]')
    lis_data = []
    for i in content:
        img_href = i.xpath('./div[@class="p-img"]/a/@href')[0]
        price = i.xpath('./div[@class="p-price"]/strong/i//text()')[0]
        title = i.xpath('./div[@class="p-name p-name-type-2"]/a/em')[0].xpath('string(.)').strip()
        comments = i.xpath('./div[@class="p-commit"]/strong//text()')[0]
        shop = i.xpath('./div[@class="p-shop"]/span/a//text()')[0]
        lis = [img_href,price,title,comments,shop]
        lis_data.append(lis)
#         print(lis)
    df = pd.DataFrame(lis_data,columns=['详细链接','价格','标题','评价数量','店铺'])
    if not os.path.isfile('text.csv'):
        df.to_csv('test.csv',mode='a',encoding='utf_8_sig',index=False)
    else:
        df.to_csv('test.csv',mode='a',encoding='utf_8_sig',index=False,header=0)
    print('保存成功!')
def get_key():
    content = input('请输入你需获取的内容：')
    brand = input('请输入你需要获取内容的品牌：')
    page = int(input('请输入您需要爬取几页：'))
    i = 1
    while i<=page:
        get_page(i,content,brand)
        i+=1
if __name__=='__main__':
    get_key()