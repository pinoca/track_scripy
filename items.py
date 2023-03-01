# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrackSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class all_list(scrapy.Item):
    num = scrapy.Field()  # 单号
    trace = scrapy.Field()  # 全部痕迹信息
