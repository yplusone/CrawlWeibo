# README

## 提交物说明

| 文件           | 说明                                                 |
| -------------- | ---------------------------------------------------- |
| weibo_crawl.py | 爬取微博数据的爬虫代码文件                           |
| weibo_check.py | 爬取并验证微博数据的代码文件                         |
| table.py       | 爬取新浪财经表格数据的爬虫文件                       |
| table_check.py | 爬取并验证新浪财经表格数据的代码文件                 |
| weibo          | 此文件夹中存储爬取的微博数据，子文件分别对应某个用户 |
| table.csv      | 此文件中存储爬取的新浪财经表格数据                   |
| weibo_log.txt  | 此文件存储验证微博数据时产生的错误信息               |
| table_log.txt  | 此文件存储验证新浪财经表格数据时产生的错误信息       |
|                |                                                      |

## 运行环境

- Python 3.6

- Pycharm 2018.2.1
- JRE: 1.8.0_152-release-1248-b8 amd64
- JVM: OpenJDK 64-Bit Server VM by JetBrain s.r.o

## 代码说明

- 验证器采用边爬取数据边对比expected_result的方式进行验证，所以不会产生actual_result的文件，而是产生对比结果的log文件。
- 微博数据的爬取需要添加cookie信息。代码中的cookie信息为组员的微博cookie信息。weibo_crawl.py爬取了内容数据和文件数据。
- 新浪财经表格为动态渲染。table.py爬取了表格数据。

## 数据说明

### 微博数据

| 数据               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| 微博id             | 某个微博的id(来自新浪微博url)                                |
| 微博正文           | 微博的正文内容                                               |
| 原始图片           | 原创微博的图片，数组形式，每一个元素包含了图片的url，类型和大小。 |
| 被转发微博原始图片 | 转发的微博的图片，数组形式，每一个元素包含了图片的url，类型和大小 |
| 是否为原创微博     | True表示是原创微博，False表示不是原创微博                    |
| 发布位置           | 微博发布位置                                                 |
| 发布时间           | 微博发布时间                                                 |
| 发布工具           | 发送设备的说明                                               |
| 点赞数             | 微博的赞数                                                   |
| 转发数             | 微博的转发数                                                 |
| 评论数             | 微博的评论数                                                 |
|           |

其中，微博id，微博正文，原始图片，被转发微博原始图片，是否为原创微博，发布位置，发布时间，发布工具为验证器验证的对象。

### 新浪财经数据

爬取的基金：

| 序号 |                              [基金代码](javascript:void(0);) |                              [基金名称](javascript:void(0);) |
| ---: | -----------------------------------------------------------: | -----------------------------------------------------------: |
|    1 | [006210](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006210&country=fund) | [东方臻宝纯债债券A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006210&country=fund) |
|    2 | [006279](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006279&country=fund) | [中金瑞祥混合A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006279&country=fund) |
|    3 | [960033](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=960033&country=fund) | [农银汇理消费主题混合H](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=960033&country=fund) |
|    4 | [150195](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150195&country=fund) | [富国中证移动互联网指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150195&country=fund) |
|    5 | [150230](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150230&country=fund) | [鹏华酒分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150230&country=fund) |
|    6 | [003793](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003793&country=fund) | [泰达宏利溢利债券A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003793&country=fund) |
|    7 | [006109](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006109&country=fund) | [富荣价值精选混合A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=006109&country=fund) |
|    8 | [150174](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150174&country=fund) | [信诚中证TMT产业主题指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150174&country=fund) |
|    9 | [005911](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=005911&country=fund) | [广发双擎升级混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=005911&country=fund) |
|   10 | [150199](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150199&country=fund) | [国泰国证食品饮料行业指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150199&country=fund) |
|   11 | [002939](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=002939&country=fund) | [广发创新升级混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=002939&country=fund) |
|   12 | [150304](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150304&country=fund) | [华安创业板50指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150304&country=fund) |
|   13 | [003745](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003745&country=fund) | [广发多元新兴股票](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003745&country=fund) |
|   14 | [502002](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502002&country=fund) | [西部利得中证500等权重指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502002&country=fund) |
|   15 | [320007](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=320007&country=fund) | [诺安成长混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=320007&country=fund) |
|   16 | [519674](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519674&country=fund) | [银河创新成长混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519674&country=fund) |
|   17 | [161810](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=161810&country=fund) | [银华内需精选混合(LOF)](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=161810&country=fund) |
|   18 | [519727](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519727&country=fund) | [交银成长30混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519727&country=fund) |
|   19 | [001071](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001071&country=fund) | [华安媒体互联网混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001071&country=fund) |
|   20 | [162703](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=162703&country=fund) | [广发小盘成长混合(LOF)](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=162703&country=fund) |
|   21 | [519778](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519778&country=fund) | [交银经济新动力混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519778&country=fund) |
|   22 | [001410](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001410&country=fund) | [信达澳银新能源产业股票](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001410&country=fund) |
|   23 | [050022](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=050022&country=fund) | [博时回报灵活配置混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=050022&country=fund) |
|   24 | [502012](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502012&country=fund) | [易方达证券公司分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502012&country=fund) |
|   25 | [161903](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=161903&country=fund) | [万家行业优选混合(LOF)](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=161903&country=fund) |
|   26 | [519773](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519773&country=fund) | [交银数据产业灵活配置混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519773&country=fund) |
|   27 | [003962](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003962&country=fund) | [易方达瑞程混合C](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003962&country=fund) |
|   28 | [257070](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=257070&country=fund) | [国联安优选行业混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=257070&country=fund) |
|   29 | [000404](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=000404&country=fund) | [易方达新兴成长混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=000404&country=fund) |
|   30 | [003961](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003961&country=fund) | [易方达瑞程混合A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003961&country=fund) |
|   31 | [519005](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519005&country=fund) | [海富通股票混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=519005&country=fund) |
|   32 | [150206](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150206&country=fund) | [鹏华中证国防指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=150206&country=fund) |
|   33 | [003516](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003516&country=fund) | [国泰融安多策略灵活配置混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003516&country=fund) |
|   34 | [050010](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=050010&country=fund) | [博时特许价值混合A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=050010&country=fund) |
|   35 | [001959](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001959&country=fund) | [华商乐享互联混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=001959&country=fund) |
|   36 | [502050](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502050&country=fund) | [易方达上证50指数分级B](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=502050&country=fund) |
|   37 | [003889](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003889&country=fund) | [汇安丰泽混合A](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003889&country=fund) |
|   38 | [003890](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003890&country=fund) | [汇安丰泽混合C](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003890&country=fund) |
|   39 | [460005](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=460005&country=fund) | [华泰柏瑞价值增长混合](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=460005&country=fund) |
|   40 | [003956](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003956&country=fund) | [南方现代教育股票](http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=003956&country=fund) |

| 数据     | 说明                             |
| -------- | -------------------------------- |
| 日期     | 2019/02/19到2019/12/24期间的数据 |
| 单位净值 | 某日零时统计的单位净值信息       |
| 累计净值 | 某日零时统计的累计净值信息       |
| 基金代码 | 基金代码                         |
| 基金名称 | 基金名称                         |
|          |                                  |