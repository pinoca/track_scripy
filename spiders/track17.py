import json
import time
import scrapy
import requests
from scrapy.http import JsonRequest
import pandas as pd
import pymongo
from scrapy.utils.project import get_project_settings
import items
import mongoengine
from mitm_tool import webbrowser_request, mitm_track17

# 能爬取的运营商
carrier_code_number_dict = {
    "ARAMEX": 100006,
    "BRT": 100026,
    "DHL": 100001,
    "DHLDE": 7041,
    "DHLUK": 100152,
    "DPDDE": 100007,
    "DPDUK": 100010,
    "DPEX": 100014,
    "FETCHR": 100083,
    "FEDEX": 100003,
    "GLS": 100005,
    "HERMES": 100018,
    "MGOSHIP": 190525,
    "OCSCHINA": 190420,
    "OULALA": 190649,
    "PARCELFORCE": 11033,
    "SAGAWA": 100040,
    "SKYNET": 100025,
    "TNT": 100004,
    "TNTAU": 100200,
    "TOLL": 100009,
    "UKMAIL": 100050,
    "UPS": 100002,
    "USPS": 21051,
    "UPS-MAIL": 100398,
    "YAMATO": 100062,
    "YODEL": 100017,
    "CHINA-POST": 3011,
    "CORREIOS": 2151,
    "LAPOSTE": 6051,
    "AUSPOST": 1151,
    "POSTNL": 14044,
    "CAINIAO": 190271,
    "SEINO": 100171,
    "SF": 100012,
    "EMS": 3013,
}

# 抓包的cookie文件存放路径
cookies_path = (
    "D:/Work_Space/scrapy_system/track_spiders/track_spiders/mitm_tool/cookies.txt"
)

# mitmproxy工具配置
mitm_url = "https://t.17track.net/zh-cn?nums=274515026840"
mitm_file_path = "D:/Work_Space/scrapy_system/track_spiders/track_spiders/mitm_tool"
mitm_file_name = "mitm_track17.py"

# 要爬取的单号，格式为{"单号"："运营商"}
track_number = {}


class track17(scrapy.Spider):
    name = "track17"

    def __init__(self, **kwargs):
        """
        :param kwargs: 无参数输入，自己设置需要的参数。
        """
        super().__init__(**kwargs)
        print("爬虫程序在初始化")
        self.settings = get_project_settings()
        # trackinfo.shape[0]
        self.cookies = self.get_cookies()
        # 标记是否拿代理IP，空为拿，不为空为不拿，默认为第一次拿IP
        self.proxies = {}
        # 代理更新时间，用于查看代理是否更改
        self.proxies_time = 0
        # ip更换次数
        self.psum = 0
        # 抓取网页的数据存储
        address_keys = [
            "name",
            "country",
            "state",
            "city",
            "address1",
            "address2",
            "address3",
            "postcode",
        ]
        self.address = {i: "" for i in address_keys}
        traces_krys = ["time", "info", "status", "address"]
        self.traces = {i: "" for i in traces_krys}

    def start_requests(self):
        """
        网站请求url生成函数，不断生成url发送到调度队列中。
        :return:
        """
        print("爬虫程序请求在初始化")
        url = "https://t.17track.net/restapi/track"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
            "Content-Type": "application/json",
            "origin": "https://t.17track.net",
            "referer": "https://t.17track.net/zh-cn",
            "cookie": "country=CN; _yq_bid=G-337A4B082A463181; v5_Culture=zh-cn; _ga=GA1.2.616261274.1652772238; __gads=ID=8fdc2ebed088bab8:T=1652772239:S=ALNI_MbOYYu3iZJPGamK7-FH5tHC86emtw; v5_TranslateLang=zh-Hans; v5_HisExpress=100010; _gid=GA1.2.28480464.1653879672; __gpi=UID=0000059c9ae69124:T=1653099004:RT=1654066907:S=ALNI_MbWICMevx_7YSORh2X8WPk3BWz0AQ; _gat_cnGa=1; Last-Event-ID=657572742f3031352f30613763393265313138312f396463353532303432353a363530343236363037323a65736c61663a6c6c616d732d736c6f6f742d71791723656fa9b04fd120d4",
        }
        # 遍历要爬取的单号信息
        date_dict = {
            "data": [{"num": "15501936183108", "fc": "100010", "sc": 0}],
            "guid": "",
            "timeZoneOffset": -480,
        }
        # 每次更新都更新Ip
        self.proxies = {}
        print("更新开始" + str(track_number))
        for index in range(len(track_number)):
            info = track_number.popitem()
            if info[1] in carrier_code_number_dict.keys():
                date_dict["data"][0]["num"] = info[0]
                date_dict["data"][0]["fc"] = str(carrier_code_number_dict[info[1]])
                yield JsonRequest(
                    url,
                    data=date_dict,
                    headers=headers,
                    callback=self.parse,
                    dont_filter=True,
                )
        print("更新结束")

    def parse(self, response, *args, **kwargs):
        """
        此函数主要处理track17网站返回的路由信息成标准的储存格式，没有存在的值设置为默认值。
        将处理好的数据通过”yield“传输到管道中
        :param response: 网站的响应体
        :param args:一个非键值对的可变数量的参数列表
        :param kwargs:将不定长度的键值对，作为参数传递
        :return:
        """
        trace_dict = json.loads(response.text)
        if trace_dict["ret"] == -7:
            print("单号格式错误")
            pass
        if trace_dict["ret"] == 1:
            # #判断数据库中是否有数据，1为没有 需要等待网站爬取
            if trace_dict["dat"][0]["delay"] == 0:
                try:
                    # item对象实例化
                    date = items.all_list()
                    trace_detail = []
                    once = []
                    # 处理日期数据为十位时间戳,并提取出时间和包裹信息
                    for j in range(len(trace_dict["dat"][0]["track"]["z1"])):
                        trace_dict["dat"][0]["track"]["z1"][j]["a"] = int(
                            time.mktime(
                                time.strptime(
                                    trace_dict["dat"][0]["track"]["z1"][j]["a"],
                                    "%Y-%m-%d %H:%M",
                                )
                            )
                        )
                        once.append(trace_dict["dat"][0]["track"]["z1"][j]["a"])
                        once.append(
                            trace_dict["dat"][0]["track"]["z1"][j]["c"]
                            + ","
                            + trace_dict["dat"][0]["track"]["z1"][j]["d"]
                            + ","
                            + trace_dict["dat"][0]["track"]["z1"][j]["z"]
                        )
                        trace_detail.append(once)
                        once = []
                    # 把处理好的数据都赋给item，由item提交给管道
                    # 拿到运营商名字
                    for k, v in carrier_code_number_dict.items():
                        if v == trace_dict["id"]:
                            date["num"] = [
                                trace_dict["dat"][0]["no"],
                                trace_dict["dat"][0]["track"]["zex"]["dtD"],
                                trace_dict["dat"][0]["track"]["zex"]["dtP"],
                                k,
                            ]
                    date["trace"] = trace_detail
                    yield date
                except:
                    print("处理失败")
                    pass
        else:
            pass

    def process_response_cheak(self, request, response) -> bool:
        """
        :param request: 请求体
        :param response 请求回来的响应体
        判断相应的数据里是否含有路由信息，如果是附带信息就返回Ture，否则为False
        """
        trace_dict = json.loads(response.text)
        # 判断是否拿到数据
        if trace_dict["ret"] != 1:
            # ret = 4可能为Cookie封禁
            if trace_dict["ret"] == -4:
                print("cookie封禁")
                # 可能为Cookie封禁，尝试更换Cookie,使用mitm_tool截取数据包
                self.cookies = self.get_cookies()
                return False
            if trace_dict["ret"] == -7:
                print("单号错误")
                # 返回体msg为”numNon“为改单号格式错误
                return True
            if trace_dict["ret"] == -5:
                # 返回体msg为”UIP“为IP封禁
                print("IP封禁")
                if request.meta["proxy_time"] == self.proxies_time:
                    self.proxies = {}
                return False
            else:
                # 代理设置为空,更换代理
                self.proxies = {}
                return False
        if trace_dict["dat"][0]["delay"] != 0:
            print("数据库没有")
            # 数据库没有重新返回
            return False
        return True

    def get_cookies(self) -> dict:
        """
        通过抓包工具来抓取需要的cookies字段，bro对象输入需要抓取的包的连接，抓包文件路径，抓包文件名字。
        :return:返回处理好的cookies字典。
        """
        webbrowser_request.bro().bro_get(
            url=mitm_url, file_path=mitm_file_path, file_name=mitm_file_name
        )
        with open(cookies_path, "r") as f:
            cookie = f.read()
            f.close()
        return mitm_track17.parse_cookies(cookie)
