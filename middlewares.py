# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import requests
from scrapy import signals
from twisted.internet.error import TimeoutError

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# 代理服务器的请求api
proxies_url = "http://www.siyetian.com/index/apis_get.html?token=gHbi1STqFEMNpWSx4kanRzTR1STqFUeNpWQx0kaZFzTEF0MNp2Yw4keFJzTE1kM.QN4UTOxEDM2YTM&limit=1&type=0&time=10&split=0&split_text=&area=0&repeat=0&isp="


class TrackSpidersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TrackSpidersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        if response.status // 100 != 2:
            print("失败")
            return request
        if spider.process_response_cheak(request, response):
            return response
        else:
            return request

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception, TimeoutError):
            self.test_proxy_useful(request.meta, request, spider)
            print(exception)
            print("重发一次")
            # return request
        pass

    def test_proxy_useful(self, meta, request, spider):
        proxy = {"http": meta["proxy"], "https": meta["proxy"]}
        if request.meta["proxy_time"] == spider.proxies_time:
            try:
                requests.get(url="https://www.baidu.com/", proxies=proxy, timeout=5)
            except:
                print(request.body)
                print("过期了")
                spider.proxies = {}

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        # 拿一次新代理
        if spider.proxies:
            pass
        else:
            spider.proxies = self.get_proxies(spider)
        request.meta["proxy"] = spider.proxies
        request.meta["proxy_time"] = spider.proxies_time
        request.meta["dont_retry"] = False
        # request.meta['max_retry_times'] = spider.settings["MAX_RETRY_TIME"]
        request.cookies = spider.cookies

    def get_proxies(self, spider):  # 代理服务器
        print("试着 拿")
        res = requests.get(proxies_url, timeout=5)
        spider.proxies_time = int(time.time())
        proxies = "http://{}".format(res.text.replace("\r\n", ""))
        spider.psum += 1
        print("更改{}次IP".format(spider.psum))
        return proxies


class My_RetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        self.test_proxy_useful(request.meta, spider)
        print("---------------在试了 在试了---------------------", exception, request.body)
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get(
            "dont_retry", False
        ):
            return self._retry(request, exception, spider)

    def test_proxy_useful(self, meta, spider):
        proxy = {"http": meta["proxy"], "https": meta["proxy"]}
        try:
            requests.get(url="https://www.baidu.com/", proxies=proxy, timeout=3)
        except:
            print("过期了")
            spider.proxies = {}
