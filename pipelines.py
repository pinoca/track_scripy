# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mongoengine
from models import Tracker
import time
from twisted.internet import reactor, defer


class TrackSpidersPipeline:
    def __init__(self):
        pass

    def process_item(self, item, spider):
        """
        功能：将格式化传入的数据处理后，存入书库
        :param item: item数据内顺序为[[单号，送达时间戳，包裹打包时间戳]，[包裹详细信息时间，包裹详细信息内容]]
        :param spider: 传入管道的爬虫信息
        :return:
        """
        crawl_list = dict(item)
        # 开始格式化traces字段
        try:
            # 格式化的字典
            f_traces = {}
            Tracker.objects.filter(
                tracking_number=crawl_list["num"][0], carrier_code=crawl_list["num"][3]
            )[0].update(traces=[])
            # 用于存入数据库的
            d_traces = []
            for i in range(len(crawl_list["trace"])):
                f_traces["time"] = crawl_list["trace"][i][0]
                f_traces["info"] = crawl_list["trace"][i][1]
                f_traces["status"] = "in_transit"
                f_traces["address"] = []
                d_traces.append(f_traces)
                f_traces = {}
            # 更新数据库操作,判断是否有包裹到达时间戳
            if crawl_list["num"][1]:
                d_traces[0]["status"] = "delivered"
                Tracker.objects.filter(
                    tracking_number=crawl_list["num"][0],
                    carrier_code=crawl_list["num"][3],
                )[0].update(
                    traces=d_traces,
                    status="delivered",
                    tracking_number=crawl_list["num"][0],
                    delivered_time=crawl_list["num"][1],
                    pickup_time=crawl_list["num"][2],
                    updated=int(time.time()),
                )
            else:
                Tracker.objects.filter(
                    tracking_number=crawl_list["num"][0],
                    carrier_code=crawl_list["num"][3],
                )[0].update(
                    traces=d_traces,
                    status="in_transit",
                    tracking_number=crawl_list["num"][0],
                    delivered_time=crawl_list["num"][1],
                    pickup_time=crawl_list["num"][2],
                    updated=int(time.time()),
                )
            print(crawl_list["num"][0] + "处理完成")
        except:
            print("traces格式化发生错误，呜呜呜 错了错了 这就改")
        return item

    def open_spider(self, spider):
        mongoengine.connect(
            spider.settings["MONGODB_DB"], host=spider.settings["MONGODB_HOST"]
        )  # 连接的数据库名称

    def close_spider(self, spider):
        mongoengine.disconnect(spider.settings["MONGODB_DB"])
