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
import pandas as pd
import numpy as np
import os
import sys

def getFunddata(symbol, Maxpage):
    urlhead = "http://stock.finance.sina.com.cn/fundInfo/api/openapi." \
              "php/CaihuiFundInfoService.getNav?callback=jQuery1112044331086053450575_" \
              "1577193543101&symbol=000311&datefrom=&dateto=&page="

    data = []

    # Get data from Sina
    for i in range(Maxpage):
        url = u"http://stock.finance.sina.com.cn/fundInfo/api/openapi." \
              "php/CaihuiFundInfoService.getNav?callback=jQuery1112044331086053450575_" \
              "1577193543101&symbol=%s&datefrom=&dateto=&page=%s&_=1577193543115" % (symbol, str(i + 1))
        html = requests.get(url).content
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

def write_bug(fund,info,originaldata,nowdata):
    file_dir = os.path.split(
        os.path.realpath(__file__))[0] + os.sep
    file_path = file_dir + './stock/基金历史信息log.txt'
    content = u'基金=%s中信息：%s出现问题。原来数据为：%s，现在数据为：%s\n' % (fund,info,originaldata,nowdata)
    print(content)
    with open(file_path, 'ab') as f:
        f.write(content.encode(sys.stdout.encoding))

'''融资融券数据爬取对象'''
class Stockaa():

    def __init__(self):
        self.begin_date = datetime.date(2019, 6, 1)   #爬取起始时间
        self.end_date = datetime.date(2019, 12, 29)   #爬取结束时间
        self.stockie = []
        self.flag=0
        self.expected_data=None

    def crawl(self):
        for i in range((self.end_date - self.begin_date).days + 1):
            day = self.begin_date + datetime.timedelta(days=i)
            self.crawl_day(str(day))
            self.check_day()
            #self.write_csv(str(day))
            print("finish "+str(day))
            self.initialize()


    def initialize(self):
        self.stockie=[]

    def crawl_day(self,day):
        '''爬取某一天融资融券数据'''
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

    def check(self):
        '''验证所有融资融券数据'''
        self.expected_data = pd.read_csv('./stock/融资融券数据.csv')
        self.crawl()

    def check_day(self):
        '''验证某日融资融券数据'''
        for row in self.stockie:
            time=datetime.datetime.strptime(row[0], '%Y-%m-%d')
            year = str(int(time.strftime('%Y')))
            month = str(int(time.strftime('%m')))
            day = str(int(time.strftime('%d')))
            time=year + '/' + month + '/' + day
            index=np.where(self.expected_data['日期']==time)[0]
            id_index=-1
            for i in index:
                if int(self.expected_data['股票代码'][i])==int(row[2]):
                    id_index=i
                    break
            if id_index!=-1:
                '''对于爬取到的信息进行验证'''
                if row[4]!='--' and float(row[4].replace(',',''))!=float(self.expected_data['融资-余额（元）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融资-余额（元）',self.expected_data['融资-余额（元）'][id_index],row[4])
                if float(row[5].replace(',',''))!=float(self.expected_data['融资-买入额（元）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融资-买入额（元）',self.expected_data['融资-买入额（元）'][id_index],row[5])
                if row[6]!='--' and float(row[6].replace(',',''))!=float(self.expected_data['融资-偿还额（元）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融资-偿还额（元）',self.expected_data['融资-偿还额（元）'][id_index],row[6])
                if row[7]!='--' and float(row[7].replace(',',''))!=float(self.expected_data['融券-余量金额（元）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融券-余量金额（元）',self.expected_data['融券-余量金额（元）'][id_index],row[7])
                if float(row[8].replace(',',''))!=float(self.expected_data['融券余量（股）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融券余量（股）',self.expected_data['融券余量（股）'][id_index],row[8])
                if float(row[9].replace(',',''))!=float(self.expected_data['融券-卖出股（股）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融券-卖出股（股）',self.expected_data['融券-卖出股（股）'][id_index],row[9])
                if row[10]!='--' and float(row[10].replace(',',''))!=float(self.expected_data['融券-偿还量（股）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融券-偿还量（股）',self.expected_data['融券-偿还量（股）'][id_index],row[10])
                if row[11]!='--' and float(row[11].replace(',',''))!=float(self.expected_data['融券-融券金额（元）'][id_index].replace(',','')):
                    self.write_bug(row[3],time,'融券-融券金额（元）',self.expected_data['融券-融券金额（元）'][id_index],row[11])

    def write_bug(self,stockname,day,tag,origindata,nowdata):
        file_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep
        file_path = file_dir + './stock/融资融券数据log.txt'
        content = u'股票%s在%s日的数据字段%s出现问题。原来数据为：%s，现在数据为：%s' % (stockname,day,tag,origindata,nowdata)
        print(content)
        with open(file_path, 'ab') as f:
            f.write(content.encode(sys.stdout.encoding))

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
                    self.check_one_page()
                    #self.write_csv()
                    self.initialize()

    def crawl_one_page(self,url):
        html = requests.get(url).content.decode('GBK')
        soup = BeautifulSoup(str(html), "html.parser")
        data = soup.find_all('tr')
        count = 0
        for tr in data:
            count = count + 1
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
                    return

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
            with open('./stock/上市公司业绩公告.csv',
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
    def check(self):
        self.expected_data = pd.read_csv('./stock/上市公司业绩公告3.csv')
        self.crawl()

    def check_one_page(self):
        for row in self.rows:
            index=np.where(self.expected_data['披露日期']==row[2])[0]
            id_index=-1
            for i in index:
                if int(self.expected_data['股票代码'][i])==int(row[0]):
                    id_index=i
                    break
            if id_index!=-1:
                '''对于爬取到的信息进行验证'''
                if row[3]!='--' and float(row[3])!=float(self.expected_data['每股收益（元）'][id_index]):
                    self.write_bug(row[1],row[2],'每股收益（元）',self.expected_data['每股收益（元）'][id_index],row[3])
                if row[4]!='--' and float(row[4])!=float(self.expected_data['营业收入（万元）'][id_index]):
                    self.write_bug(row[1],row[2],'营业收入（万元）',self.expected_data['营业收入（万元）'][id_index],row[4])
                if row[5]!='--' and float(row[5])!=float(self.expected_data['营业收入同比（%）'][id_index]):
                    self.write_bug(row[1],row[2],'营业收入同比（%）',self.expected_data['营业收入同比（%）'][id_index],row[5])
                if row[6]!='--' and float(row[6])!=float(self.expected_data['净利润（万元）'][id_index]):
                    self.write_bug(row[1],row[2],'净利润（万元）',self.expected_data['净利润（万元）'][id_index],row[6])
                if row[7]!='--' and float(row[7])!=float(self.expected_data['净利润同比（%）'][id_index]):
                    self.write_bug(row[1],row[2],'净利润同比（%）',self.expected_data['净利润同比（%）'][id_index],row[7])
                if row[8]!='--' and float(row[8])!=float(self.expected_data['每股净资产（元）'][id_index]):
                    self.write_bug(row[1],row[2],'每股净资产（元）',self.expected_data['每股净资产（元）'][id_index],row[8])
                if row[9]!='--' and float(row[9])!=float(self.expected_data['净资产收益率（%）'][id_index]):
                    self.write_bug(row[1],row[2],'净资产收益率（%）',self.expected_data['净资产收益率（%）'][id_index],row[9])
                if row[10]!='--' and float(row[10])!=float(self.expected_data['每股现金流（元）'][id_index]):
                    self.write_bug(row[1],row[2],'每股现金流（元）',self.expected_data['每股现金流（元）'][id_index],row[10])
                if row[11]!='--' and float(row[11])!=float(self.expected_data['毛利率（%）'][id_index]):
                    self.write_bug(row[1],row[2],'毛利率（%）',self.expected_data['毛利率（%）'][id_index],row[11])
                if row[12]!='--' and row[12]!=self.expected_data['分配方案'][id_index]:
                    self.write_bug(row[1],row[2],'分配方案',self.expected_data['分配方案'][id_index],row[12])
                if row[13]!='--' and row[13]!=self.expected_data['明细'][id_index]:
                    self.write_bug(row[1],row[2],'明细',self.expected_data['明细'][id_index],row[13])

                if row[14]!='--' and row[14]!=self.expected_data['PDF报告'][id_index]:
                    self.write_bug(row[1],row[2],'PDF报告',self.expected_data['PDF报告'][id_index],row[14])
                try:
                    if row[15]!='null' and self.expected_data['文件大小'][id_index]!='null' and int(row[15])!=int(self.expected_data['文件大小'][id_index]):
                        self.write_bug(row[1],row[2],'文件大小',self.expected_data['文件大小'][id_index],row[15])
                    if row[16]!='--' and row[16]!=self.expected_data['文件类型'][id_index]:
                        self.write_bug(row[1],row[2],'文件类型',self.expected_data['文件类型'][id_index],row[16])
                    if row[17]!='--' and row[17]!=self.expected_data['文件最后修改时间'][id_index]:
                        self.write_bug(row[1],row[2],'文件最后修改时间',self.expected_data['文件最后修改时间'][id_index],row[17])
                except Exception as e:
                    print('Error: ', e)
                    traceback.print_exc()


    def write_bug(self,stockname,day,tag,origindata,nowdata):
        file_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep
        file_path = file_dir + './stock/上市公司业绩公告log.txt'
        content = u'股票%s在%s日的数据字段%s出现问题。原来数据为：%s，现在数据为：%s\n' % (stockname,day,tag,origindata,nowdata)
        print(content)
        with open(file_path, 'ab') as f:
            f.write(content.encode(sys.stdout.encoding))
def main():
    try:
        '''验证基金历史信息'''
        # expected_data = pd.read_csv('./stock/基金历史信息.csv')
        # res=getFunds()
        # for i in range(len(res)):
        #     print(res[i]['symbol'])
        #     result=getFunddata(res[i]['symbol'],1)
        #     index=np.where(expected_data['基金代码']==res[i]['symbol'])[0]
        #     for r in result:
        #         time=r['fbrq']
        #         time_index=-1
        #         for i in index:
        #             if expected_data['日期'][i]==time:
        #                 time_index=i
        #         if time_index!=-1:
        #             '''对于爬取到的信息进行验证'''
        #             if round(float(r['jjjz']),3)!=round(float(expected_data['单位净值'][time_index]),3):
        #                 write_bug(expected_data['基金名称'][time_index],'单位净值',expected_data['单位净值'][time_index],r['jjjz'])
        #             if round(float(r['ljjz']),3)!=round(float(expected_data['累计净值'][time_index]),3):
        #                 write_bug(expected_data['基金名称'][time_index],'累计净值',expected_data['累计净值'][time_index],r['ljjz'])
        '''验证融资融券数据'''
        # stock = Stockaa()
        # stock.check()
        '''验证上市公司业绩公告数据'''
        file=File()
        file.check()

    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()
