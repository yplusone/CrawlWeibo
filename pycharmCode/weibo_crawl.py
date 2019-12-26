import csv
import os
import random
import re
import sys
import traceback
from collections import OrderedDict
from datetime import datetime, timedelta
from time import sleep
import io
from urllib import request
from PIL import Image

import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from tqdm import tqdm


class Weibo():
    def __init__(self):
        """Weibo类初始化"""
        since_date = "2017-01-01"
        self.since_date = since_date  # 起始时间，即爬取发布日期从该值到现在的微博，形式为yyyy-mm-dd
        self.cookie = {'Cookie': "ALF=1579705075; SUB=_2A25zBKWkDeRhGeRM7FcZ8y7OyDyIHXVQBsvsrDV6PUNbktANLVnhkW1NU9moMyKhvITEyUugP5oz7i5O1dmgv_Gh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFms3M2Djd6QgTcSdZ2i7id5JpX5KzhUgL.FozES0-Re05Ee052dJLoIX2LxK-L1K-L122LxK-L1K-L122LxK-L1K-L128yi--fiK.0i-2ci--fiK.0i-2ci--fiK.0i-2ci--fiK.0i-2cd7tt; SUHB=0HTwhSzVzD1jBB; SSOLoginState=1577113076; _T_WM=73092647507; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174; WEIBOCN_FROM=1110106030"}
        self.user_id_list = ["1893801487"]
        self.user_id = ''
        self.user = {}
        self.got_num = 0
        self.weibo = []
        self.weibo_id_list = []

    def deal_html(self, url):
        """处理html"""
        try:
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def deal_garbled(self, info):
        """处理乱码"""
        try:
            info = (info.xpath('string(.)').replace(u'\u200b', '').encode(
                sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
            return info
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_nickname(self):
        """获取用户昵称"""
        try:
            url = 'https://weibo.cn/%s/info' % (self.user_id)
            selector = self.deal_html(url)
            nickname = selector.xpath('//title/text()')[0]
            nickname = nickname[:-3]
            self.user['nickname'] = nickname
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def print_user_info(self):
        """打印微博用户信息"""
        print(u'用户昵称: %s' % self.user['nickname'])
        print(u'用户id: %s' % self.user['id'])
        print(u'微博数: %d' % self.user['weibo_num'])
        print(u'关注数: %d' % self.user['following'])
        print(u'粉丝数: %d' % self.user['followers'])

    def get_user_info(self, selector):
        """获取用户昵称、微博数、关注数、粉丝数"""
        try:
            self.get_nickname()  # 获取用户昵称
            user_info = selector.xpath("//div[@class='tip2']/*/text()")
            weibo_num = int(user_info[0][3:-1])
            following = int(user_info[1][3:-1])
            followers = int(user_info[2][3:-1])
            self.user['weibo_num'] = weibo_num
            self.user['following'] = following
            self.user['followers'] = followers
            self.user['id'] = self.user_id
            print('*' * 100)
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_page_num(self, selector):
        """获取微博总页数"""
        try:
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(
                    selector.xpath("//input[@name='mp']")[0].attrib['value'])
            return page_num
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_long_weibo(self, weibo_link):
        """获取长原创微博"""
        try:
            selector = self.deal_html(weibo_link)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = self.deal_garbled(info)
            wb_time = info.xpath("//span[@class='ct']/text()")[0]
            weibo_content = wb_content[wb_content.find(':') +
                                       1:wb_content.rfind(wb_time)]
            return weibo_content
        except Exception as e:
            return u'网络出错'
            print('Error: ', e)
            traceback.print_exc()

    def get_original_weibo(self, info, weibo_id):
        """获取原创微博"""
        try:
            weibo_content = self.deal_garbled(info)
            weibo_content = weibo_content[:weibo_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                weibo_link = 'https://weibo.cn/comment/' + weibo_id
                wb_content = self.get_long_weibo(weibo_link)
                if wb_content:
                    weibo_content = wb_content
            return weibo_content
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_long_retweet(self, weibo_link):
        """获取长转发微博"""
        try:
            wb_content = self.get_long_weibo(weibo_link)
            weibo_content = wb_content[:wb_content.rfind(u'原文转发')]
            return weibo_content
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_retweet(self, info, weibo_id):
        """获取转发微博"""
        try:
            wb_content = self.deal_garbled(info)
            wb_content = wb_content[wb_content.find(':') +
                                    1:wb_content.rfind(u'赞')]
            wb_content = wb_content[:wb_content.rfind(u'赞')]
            a_text = info.xpath('div//a/text()')
            if u'全文' in a_text:
                weibo_link = 'https://weibo.cn/comment/' + weibo_id
                weibo_content = self.get_long_retweet(weibo_link)
                if weibo_content:
                    wb_content = weibo_content
            retweet_reason = self.deal_garbled(info.xpath('div')[-1])
            retweet_reason = retweet_reason[:retweet_reason.rindex(u'赞')]
            original_user = info.xpath("div/span[@class='cmt']/a/text()")
            if original_user:
                original_user = original_user[0]
                wb_content = (retweet_reason + '\n' + u'原始用户: ' +
                              original_user + '\n' + u'转发内容: ' + wb_content)
            else:
                wb_content = retweet_reason + '\n' + u'转发内容: ' + wb_content
            return wb_content
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def is_original(self, info):
        """判断微博是否为原创微博"""
        is_original = info.xpath("div/span[@class='cmt']")
        if len(is_original) > 3:
            return False
        else:
            return True

    def get_weibo_content(self, info, is_original):
        """获取微博内容"""
        try:
            weibo_id = info.xpath('@id')[0][2:]
            if is_original:
                weibo_content = self.get_original_weibo(info, weibo_id)
            else:
                weibo_content = self.get_retweet(info, weibo_id)
            return weibo_content
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_publish_place(self, info):
        """获取微博发布位置"""
        try:
            div_first = info.xpath('div')[0]
            a_list = div_first.xpath('a')
            publish_place = u'无'
            for a in a_list:
                if ('place.weibo.com' in a.xpath('@href')[0]
                        and a.xpath('text()')[0] == u'显示地图'):
                    weibo_a = div_first.xpath("span[@class='ctt']/a")
                    if len(weibo_a) >= 1:
                        publish_place = weibo_a[-1]
                        if (u'视频' == div_first.xpath(
                                "span[@class='ctt']/a/text()")[-1][-2:]):
                            if len(weibo_a) >= 2:
                                publish_place = weibo_a[-2]
                            else:
                                publish_place = u'无'
                        publish_place = self.deal_garbled(publish_place)
                        break
            return publish_place
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_publish_time(self, info):
        """获取微博发布时间"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
            publish_time = str_time.split(u'来自')[0]
            if u'刚刚' in publish_time:
                publish_time = datetime.now().strftime('%Y-%m-%d %H:%M')
            elif u'分钟' in publish_time:
                minute = publish_time[:publish_time.find(u'分钟')]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() -
                                minute).strftime('%Y-%m-%d %H:%M')
            elif u'今天' in publish_time:
                today = datetime.now().strftime('%Y-%m-%d')
                time = publish_time[3:]
                publish_time = today + ' ' + time
                if len(publish_time) > 16:
                    publish_time = publish_time[:16]
            elif u'月' in publish_time:
                year = datetime.now().strftime('%Y')
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = year + '-' + month + '-' + day + ' ' + time
            else:
                publish_time = publish_time[:16]
            return publish_time
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_publish_tool(self, info):
        """获取微博发布工具"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
            if len(str_time.split(u'来自')) > 1:
                publish_tool = str_time.split(u'来自')[1]
            else:
                publish_tool = u'无'
            return publish_tool
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_weibo_footer(self, info):
        """获取微博点赞数、转发数、评论数"""
        try:
            footer = {}
            pattern = r'\d+'
            str_footer = info.xpath('div')[-1]
            str_footer = self.deal_garbled(str_footer)
            str_footer = str_footer[str_footer.rfind(u'赞'):]
            weibo_footer = re.findall(pattern, str_footer, re.M)

            up_num = int(weibo_footer[0])
            footer['up_num'] = up_num

            retweet_num = int(weibo_footer[1])
            footer['retweet_num'] = retweet_num

            comment_num = int(weibo_footer[2])
            footer['comment_num'] = comment_num
            return footer
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def extract_picture_urls(self, info, weibo_id):
        """提取微博原始图片url"""
        try:
            a_list = info.xpath('div/a/@href')
            first_pic = 'https://weibo.cn/mblog/pic/' + weibo_id + '?rl=0'
            all_pic = 'https://weibo.cn/mblog/picAll/' + weibo_id + '?rl=1'
            if first_pic in a_list:
                if all_pic in a_list:
                    selector = self.deal_html(all_pic)
                    preview_picture_list = selector.xpath('//img/@src')
                    picture_list = [
                        p.replace('/thumb180/', '/large/')
                        for p in preview_picture_list
                    ]
                    picture_urls = picture_list
                else:
                    if info.xpath('.//img/@src'):
                        preview_picture = info.xpath('.//img/@src')[-1]
                        picture_urls = preview_picture.replace(
                            '/wap180/', '/large/')
                    else:
                        sys.exit(
                            u"爬虫微博可能被设置成了'不显示图片'，请前往"
                            u"'https://weibo.cn/account/customize/pic'，修改为'显示'"
                        )
            else:
                picture_urls = []
            pictures=[]
            for pic_url in picture_list:
                file = request.urlopen(pic_url)
                tmpIm = io.BytesIO(file.read())
                img = Image.open(tmpIm)
                picture={}
                picture['url'] = pic_url
                picture['type'] = img.format
                picture['size'] = img.size
                pictures.append(picture)
            return pictures
        except Exception as e:
            return u'无'
            print('Error: ', e)
            traceback.print_exc()

    def get_picture_urls(self, info, is_original):
        """获取微博原始图片url"""
        try:
            weibo_id = info.xpath('@id')[0][2:]
            picture_urls = {}
            if is_original:
                original_pictures = self.extract_picture_urls(info, weibo_id)
                picture_urls['original_pictures'] = original_pictures
                picture_urls['retweet_pictures'] = u'无'
            else:
                retweet_url = info.xpath("div/a[@class='cc']/@href")[0]
                retweet_id = retweet_url.split('/')[-1].split('?')[0]
                retweet_pictures = self.extract_picture_urls(info, retweet_id)
                picture_urls['retweet_pictures'] = retweet_pictures
                a_list = info.xpath('div[last()]/a/@href')
                original_picture = u'无'
                for a in a_list:
                    if a.endswith(('.gif', '.jpeg', '.jpg', '.png')):
                        original_picture = a
                        break
                picture_urls['original_pictures'] = original_picture
            return picture_urls
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_one_weibo(self, info):
        """获取一条微博的全部信息"""
        try:
            weibo = OrderedDict()
            is_original = self.is_original(info)
            weibo['id'] = info.xpath('@id')[0][2:]
            weibo['content'] = self.get_weibo_content(info,
                                                      is_original)  # 微博内容
            picture_urls = self.get_picture_urls(info, is_original)
            weibo['original_pictures'] = picture_urls[
                'original_pictures']  # 原创图片url
            weibo['retweet_pictures'] = picture_urls[
                'retweet_pictures']  # 转发图片url
            weibo['original'] = is_original  # 是否原创微博
            weibo['publish_place'] = self.get_publish_place(info)  # 微博发布位置
            weibo['publish_time'] = self.get_publish_time(info)  # 微博发布时间
            weibo['publish_tool'] = self.get_publish_tool(info)  # 微博发布工具
            footer = self.get_weibo_footer(info)
            weibo['up_num'] = footer['up_num']  # 微博点赞数
            weibo['retweet_num'] = footer['retweet_num']  # 转发数
            weibo['comment_num'] = footer['comment_num']  # 评论数
            return weibo
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def print_one_weibo(self, weibo):
        """打印一条微博"""
        print(weibo['content'])
        print(u'微博发布位置：%s' % weibo['publish_place'])
        print(u'发布发布时间：%s' % weibo['publish_time'])
        print(u'发布发布工具：%s' % weibo['publish_tool'])
        print(u'点赞数：%d' % weibo['up_num'])
        print(u'转发数：%d' % weibo['retweet_num'])
        print(u'评论数：%d' % weibo['comment_num'])

    def get_one_page(self, page):
        """获取第page页的全部微博"""
        try:
            url = 'https://weibo.cn/u/%s?page=%d' % (self.user_id, page)
            selector = self.deal_html(url)
            info = selector.xpath("//div[@class='c']")
            is_exist = info[0].xpath("div/span[@class='ctt']")
            if is_exist:
                for i in range(0, len(info) - 2):
                    weibo = self.get_one_weibo(info[i])
                    if weibo:
                        if weibo['id'] in self.weibo_id_list:
                            continue
                        publish_time = datetime.strptime(
                            weibo['publish_time'][:10], "%Y-%m-%d")
                        since_date = datetime.strptime(self.since_date,
                                                       "%Y-%m-%d")
                        if publish_time < since_date:
                            return True
                        self.print_one_weibo(weibo)
                        self.weibo.append(weibo)
                        self.weibo_id_list.append(weibo['id'])
                        self.got_num += 1
                        print('-' * 100)
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_filepath(self, type):
        """获取结果文件路径"""
        try:
            file_dir = os.path.split(
                os.path.realpath(__file__)
            )[0] + os.sep + 'weibo' + os.sep + self.user['nickname']
            if type == 'img' :
                file_dir = file_dir + os.sep + type
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir)
            if type == 'img' :
                return file_dir
            file_path = file_dir + os.sep + self.user_id + '.' + type
            return file_path
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def write_log(self):
        """当程序因cookie过期停止运行时，将相关信息写入log.txt"""
        file_dir = os.path.split(
            os.path.realpath(__file__))[0] + os.sep + 'weibo' + os.sep
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + 'log.txt'
        content = u'cookie已过期，从%s到今天的微博获取失败，请重新设置cookie\n' % self.since_date
        with open(file_path, 'ab') as f:
            f.write(content.encode(sys.stdout.encoding))

    def write_csv(self, wrote_num):
        """将爬取的信息写入csv文件"""
        try:
            result_headers = [
                '微博id',
                '微博正文',
                '原始图片',
                '被转发微博原始图片',
                '是否为原创微博',
                '发布位置',
                '发布时间',
                '发布工具',
                '点赞数',
                '转发数',
                '评论数',
            ]
            result_data = [w.values() for w in self.weibo][wrote_num:]
            with open(self.get_filepath('csv'),
                      'a',
                      encoding='utf-8-sig',
                      newline='') as f:
                writer = csv.writer(f)
                if wrote_num == 0:
                    writer.writerows([result_headers])
                writer.writerows(result_data)
            print(u'%d条微博写入csv文件完毕,保存路径:' % self.got_num)
            print(self.get_filepath('csv'))
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_weibo_info(self):
        """获取微博信息"""
        try:
            url = 'https://weibo.cn/u/%s' % (self.user_id)
            selector = self.deal_html(url)
            self.get_user_info(selector)  # 获取用户昵称、微博数、关注数、粉丝数
            page_num = self.get_page_num(selector)  # 获取微博总页数
            wrote_num = 0
            page1 = 0
            random_pages = random.randint(1, 5)
            for page in tqdm(range(1, page_num + 1), desc='Progress'):
                is_end = self.get_one_page(page)  # 获取第page页的全部微博
                if is_end:
                    break

                if page % 20 == 0:  # 每爬20页写入一次文件
                    self.write_csv(wrote_num)
                    wrote_num = self.got_num

                if page - page1 == random_pages and page < page_num:
                    sleep(random.randint(6, 10))
                    page1 = page
                    random_pages = random.randint(1, 5)

            self.write_csv(wrote_num)  # 将剩余不足20页的微博写入文件
            print(u'共爬取' + str(self.got_num) + u'条微博')
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()

    def get_user_list(self, file_name):
        """获取文件中的微博id信息"""
        with open(file_name, 'rb') as f:
            lines = f.read().splitlines()
            lines = [line.decode('utf-8') for line in lines]
            user_id_list = [
                line.split(' ')[0] for line in lines
                if len(line.split(' ')) > 0 and line.split(' ')[0].isdigit()
            ]
        return user_id_list

    def initialize_info(self, user_id):
        """初始化爬虫信息"""
        self.got_num = 0
        self.weibo = []
        self.user = {}
        self.user_id = user_id
        self.weibo_id_list = []

    def start(self):
        """运行爬虫"""
        try:
            for user_id in self.user_id_list:
                self.initialize_info(user_id)
                print('*' * 100)
                self.get_weibo_info()
                print(u'信息抓取完毕')
                print('*' * 100)
        except Exception as e:
            print('Error: ', e)
            traceback.print_exc()


def main():
    try:
        wb = Weibo()
        wb.start()  # 爬取微博信息
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()


if __name__ == '__main__':
    main()