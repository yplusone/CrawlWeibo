import csv
import re
import traceback
import requests
import pandas as pd
import numpy as np
import os
import sys

def getFunddata(symbol,Maxpage):
    urlhead = "http://stock.finance.sina.com.cn/fundInfo/api/openapi." \
              "php/CaihuiFundInfoService.getNav?callback=jQuery1112044331086053450575_" \
              "1577193543101&symbol=000311&datefrom=&dateto=&page="

    data = []

    # Get data from Sina
    for i in range(Maxpage):
        url = u"http://stock.finance.sina.com.cn/fundInfo/api/openapi." \
              "php/CaihuiFundInfoService.getNav?callback=jQuery1112044331086053450575_" \
              "1577193543101&symbol=%s&datefrom=&dateto=&page=%s&_=1577193543115"%(symbol,str(i+1))
        html = requests.get(url).content
        data = data + re.findall(u'\{"fbrq.*?"\}', str(html))

    result=[]
    for i in range(len(data)):
        result.append(eval(data[i]))

    return result


def write_csv(res_dict,result,index):
    """将爬取的信息写入csv文件"""
    try:
        result_headers = [
            '日期',
            '单位净值',
            '累计净值',
            '基金代码',
            '基金名称',
        ]
        result_data=[]
        for w in range(len(result)):
            result[w]['id']=res_dict['symbol']
            result[w]['name']=res_dict['sname']
            res=[t for t in result[w].values()]
            result_data.append(res)
        with open('./table.csv',
                  'a',
                  encoding='utf-8-sig',
                  newline='') as f:
            writer = csv.writer(f)
            if index==0:
                writer.writerows([result_headers])
            writer.writerows(result_data)
        print("数据爬取成功")
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()

def getFunds():
    data=[]
    url="http://vip.stock.finance.sina.com.cn/fund_center/data/jsonp.php/" \
        "IO.XSRV2.CallbackList['6XxbX6h4CED0ATvW']/NetValue_Service.getNetVa" \
        "lueOpen?page=1&num=40&sort=nav_date&asc=0&ccode=&type2=0&type3="
    html = requests.get(url).content.decode('GBK')
    data = re.findall(u'\{symbol.*?\}', str(html))
    res=[]
    for d in data:
        dd=d.replace("symbol","\"symbol\"")
        dd=dd.replace("sname","\"sname\"")
        dd = dd.replace("per_nav", "\"per_nav\"")
        dd = dd.replace("total_nav", "\"total_nav\"")
        dd = dd.replace("yesterday_nav", "\"yesterday_nav\"")
        dd = dd.replace("nav_rate", "\"nav_rate\"")
        dd = dd.replace("nav_a", "\"nav_a\"")
        dd=dd.replace("sg_states","\"sg_states\"")
        dd = dd.replace("nav_date", "\"nav_date\"")
        dd = dd.replace("fund_manager", "\"fund_manager\"")
        dd = dd.replace("jjlx", "\"jjlx\"")
        dd = dd.replace("jjzfe", "\"jjzfe\"")
        res.append(eval(dd))
    return res

def write_bug(fund,info):
    file_dir = os.path.split(
        os.path.realpath(__file__))[0] + os.sep
    file_path = file_dir + 'log_table.txt'
    content = u'基金=%s中信息：%s出现问题\n' % (fund,info)
    print(content)
    with open(file_path, 'ab') as f:
        f.write(content.encode(sys.stdout.encoding))

def main():
    try:
        expected_data = pd.read_csv('./table.csv')
        res=getFunds()
        for i in range(len(res)):
            print(res[i]['symbol'])
            result=getFunddata(res[i]['symbol'],1)
            index=np.where(expected_data['基金代码']==res[i]['symbol'])[0]
            for r in result:
                time=r['fbrq']
                time_index=-1
                for i in index:
                    if expected_data['日期'][i]==time:
                        time_index=i
                if time_index!=-1:
                    if r['jjjz']!=expected_data['单位净值'][time_index]:
                        write_bug(expected_data['基金名称'][time_index],'单位净值')
                    if r['ljjz']!=expected_data['累计净值'][time_index]:
                        write_bug(expected_data['基金名称'][time_index],'累计净值')
            #write_csv(res[i],result,i)
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()