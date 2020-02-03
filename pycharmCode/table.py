import csv
import re
import traceback
import requests
from lxml import etree
import json
from bs4 import BeautifulSoup
import datetime
import urllib.request as urllib2
import io
from urllib import request
import time


def getFunddata(symbol, Maxpage):

    data = []

    # Get data from Sina
    for i in range(Maxpage):
        url = u"http://stock.finance.sina.com.cn/fundInfo/api/openapi." \
              "php/CaihuiFundInfoService.getNav?callback=jQuery1112044331086053450575_" \
              "1577193543101&symbol=%s&datefrom=&dateto=&page=%s&_=1577193543115" % (symbol, str(i + 1))
        while 1:
            try:
                html = requests.get(url).content
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                continue
        data = data + re.findall(u'\{"fbrq.*?"\}', str(html))

    result = []
    for i in range(len(data)):
        result.append(eval(data[i]))

    return result


def write_csv(res_dict, result, index):
    """将爬取的信息写入csv文件"""
    try:
        result_headers = [
            '日期',
            '单位净值',
            '累计净值',
            '基金代码',
            '基金名称',
        ]
        result_data = []
        for w in range(len(result)):
            result[w]['id'] = res_dict['symbol']
            result[w]['name'] = res_dict['sname']
            res = [t for t in result[w].values()]
            result_data.append(res)
        with open('./stock/基金历史信息.csv',
                  'a',
                  encoding='utf-8-sig',
                  newline='') as f:
            writer = csv.writer(f)
            if index == 0:
                writer.writerows([result_headers])
            writer.writerows(result_data)
        print("数据爬取成功")
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()

def getFunds():
    res = []
    for i in range(200):
        url="http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/" \
          "IO.XSRV2.CallbackList['6XxbX6h4CED0ATvW']/NetValue_Service.getNetVa" \
          "lueOpen?page=%s&num=40&sort=nav_date&asc=0&ccode=&type2=0&type3="%str(i+1)
        html = requests.get(url).content.decode('GBK')
        data = re.findall(u'\{symbol.*?\}', str(html))
        for d in data:
            dd = d.replace("symbol", "\"symbol\"")
            dd = dd.replace("sname", "\"sname\"")
            dd = dd.replace("per_nav", "\"per_nav\"")
            dd = dd.replace("total_nav", "\"total_nav\"")
            dd = dd.replace("yesterday_nav", "\"yesterday_nav\"")
            dd = dd.replace("nav_rate", "\"nav_rate\"")
            dd = dd.replace("nav_a", "\"nav_a\"")
            dd = dd.replace("sg_states", "\"sg_states\"")
            dd = dd.replace("nav_date", "\"nav_date\"")
            dd = dd.replace("fund_manager", "\"fund_manager\"")
            dd = dd.replace("jjlx", "\"jjlx\"")
            dd = dd.replace("jjzfe", "\"jjzfe\"")
            res.append(eval(dd))
    print(len(res))
    return res

class Stockaa():

    def __init__(self):
        self.begin_date = datetime.date(2011, 6, 1)
        self.end_date = datetime.date(2019, 12, 29)
        self.stockie = []
        self.flag=0

    def crawl(self):
        for i in range((self.end_date - self.begin_date).days + 1):
            day = self.begin_date + datetime.timedelta(days=i)
            self.crawl_day(str(day))
            self.write_csv(str(day))
            print("finish "+str(day))
            self.initialize()


    def initialize(self):
        self.stockie=[]

    def crawl_day(self,day):
        url = u"http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?tradedate="+day
        html = requests.get(url).content.decode('GBK')
        soup = BeautifulSoup(str(html), "html.parser")
        data = soup.find_all('tr')
        count = 0
        for tr in data:
            count = count + 1
            if count > 7:
                tr_child = tr.find_all('td')
                row_data = []
                row_data.append(day)
                for child in tr_child:
                    child_text = child.get_text()
                    row_data.append(child_text)
                self.stockie.append(row_data)

    def write_csv(self,day):
        """将爬取的信息写入csv文件"""
        try:
            result_headers = [
                '日期',
                '序号',
                '股票代码',
                '股票名称',
                '融资-余额（元）',
                '融资-买入额（元）',
                '融资-偿还额（元）',
                '融券-余量金额（元）',
                '融券余量（股）',
                '融券-卖出股（股）',
                '融券-偿还量（股）',
                '融券-融券金额（元）'
            ]
            with open('./stock/融资融券数据.csv',
                      'a',
                      encoding='utf-8-sig',
                      newline='') as f:
                writer = csv.writer(f)
                if self.flag == 0:
                    writer.writerows([result_headers])
                    self.flag=1
                writer.writerows(self.stockie)
            print(day+"数据爬取成功")
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

class File():

    def __init__(self):
        self.rows=[]
        self.seasons=['-03-31','-06-30','-09-30','-12-31']
        self.year_begin=2014
        self.year_end=2019
        self.max_page_num=10
        self.flag=0

    def initialize(self):
        self.rows=[]

    def crawl(self):
        for season in self.seasons:
            for year in range(self.year_end-self.year_begin+1):
                for page_index in range(self.max_page_num):
                    theyear=self.year_begin+year
                    day=str(theyear)+season
                    print(day)
                    url=u"http://finance.sina.com.cn/realstock/income_statement/%s/issued_pdate_ac_%s.html"%(day,str(page_index+1))
                    print(url)
                    self.crawl_one_page(url)
                    self.write_csv()
                    self.initialize()

    def crawl_one_page(self,url):
        while 1:
            try:
                html = requests.get(url).content.decode('GBK')
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                continue
        soup = BeautifulSoup(str(html), "html.parser")
        data = soup.find_all('tr')
        count = 0
        for tr in data:
            count = count + 1
            print(count)
            if count > 3:
                tr_child = tr.find_all('td')
                row_data = []
                child_count=0
                for child in tr_child:
                    if child_count==0 or child_count==1:
                        for a_child in child:
                            try:
                                row_data.append(a_child.get_text())
                            except Exception as e:
                                row_data.append('null')
                    elif child_count==13:
                        for a_child in child:
                            try:
                                row_data.append(a_child['href'])
                            except Exception as e:
                                row_data.append('null')
                    elif child_count == 14:
                        for a_child in child:
                            '''爬取公告文件元数据'''
                            try:
                                row_data.append(a_child['href'])
                                file_url=str(a_child['href'])
                                meta = self.getRemoteFileSize(file_url)
                                if meta!=None:
                                    row_data.append(meta['Content-Length'])
                                    row_data.append(meta['Content-Type'])
                                    row_data.append(meta['Last-Modified'])
                                else:
                                    row_data.append('null')
                                    row_data.append('null')
                                    row_data.append('null')
                            except Exception as e:
                                row_data.append('null')
                                row_data.append('null')
                                row_data.append('null')
                                row_data.append('null')
                    else:
                        child_text = child.get_text()
                        row_data.append(child_text)
                    child_count=child_count+1
                if len(row_data)!=12:   #最下面的页码一行不要
                    self.rows.append(row_data)

    def getRemoteFileSize(self,url):
        try:
            file = request.urlopen(url)
            meta=file.info()
            return meta
        except Exception as e:
            return None

    def write_csv(self):
        """将爬取的信息写入csv文件"""
        try:
            result_headers = [
                '股票代码',
                '股票名称',
                '披露日期',
                '每股收益（元）',
                '营业收入（万元）',
                '营业收入同比（%）',
                '净利润（万元）',
                '净利润同比（%）',
                '每股净资产（元）',
                '净资产收益率（%）',
                '每股现金流（元）',
                '毛利率（%）',
                '分配方案',
                '明细',
                'PDF报告',
                '文件大小',
                '文件类型',
                '文件最后修改时间'
            ]
            with open('./stock/上市公司业绩公告3.csv',
                      'a',
                      encoding='utf-8-sig',
                      newline='') as f:
                writer = csv.writer(f)
                if self.flag == 0:
                    writer.writerows([result_headers])
                    self.flag=1
                writer.writerows(self.rows)
            print("数据爬取成功")
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()
def main():
    try:
        '''爬取基金历史信息'''
        # res=getFunds()
        #
        # for i in range(len(res)):
        #     print(res[i]['symbol'])
        #     result=getFunddata(res[i]['symbol'],30)
        #     write_csv(res[i],result,i)

        '''爬取融资融券数据'''
        # stock = Stockaa()
        # stock.crawl()

        '''爬取上市公司业绩公告'''
        file=File()
        file.crawl()

    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
