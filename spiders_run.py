import threading
import time

import pymongo
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import multiprocessing
import settings
from spiders import track17
import os
from multiprocessing import Pool
import sys


def pack_number_distribute():
    """
    使用pymongo连接数据库，数据库配置文件属于同目录的settings.py文件
    功能：向各个爬虫分配快递单号
    :return:
    """
    # 连接数据库
    client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = client[settings.MONGODB_DB][settings.MONGODB_COLLECT]
    # if time.localtime().tm_hour == start_crwal_time[0]:
    # 数据库路由信息
    track_info = pd.DataFrame(list(collection.find()))
    # 一个单号的信息,要传输给爬虫的数据格式{单号：运营商}
    track_number = {}
    for i in range(track_info.shape[0]):
        # 跟上次的更新时间差距3个小时就计入更新
        if int(time.time()) - track_info["updated"][i] > 300:
            track_number[track_info["tracking_number"][i]] = track_info["carrier_code"][
                i
            ]
    print("传输单号" + str(track_number))
    track17.track_number = track_number


def spiders_run_process():
    """
    描述：用于执行爬虫功能的子进程。首先连接数据库拿到要爬取的单号，然后启动爬虫进程
    :return:
    """
    print("启动")
    pack_number_distribute()
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
    # 爬虫设置
    spider_settings = get_project_settings()
    process = CrawlerProcess(spider_settings)
    # 注册要使用的爬虫
    process.crawl(track17.track17)
    process.start()


if __name__ == "__main__":
    # 限制爬虫等待
    pool = Pool(1)
    print("主进程启动")
    # 获取进程的名称
    print("主进程name", multiprocessing.current_process())
    # 获取进程的pid
    print("主进程pid", multiprocessing.current_process().pid, os.getpid())
    time_temp = time.time()
    time_temp1 = time.time()
    pool.apply(spiders_run_process)
    while True:
        if time.time() - time_temp > 1800:
            time_temp = time.time()
            print(time.localtime().tm_min)
            a2 = time.time() - time_temp1
            pool.apply(spiders_run_process)
            print("启动子进程", a2)
            a1 = a2
