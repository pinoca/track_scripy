# sample2.py
from typing import Optional

import requests
import json
import asyncio
import sys
import time
import pymongo
from scrapy.utils.project import get_project_settings
from pyppeteer_stealth import stealth
import random
from pyppeteer.errors import *
from pyppeteer import *
from pyppeteer.launcher import DEFAULT_ARGS
import requests
import json
import datetime
import os
import copy


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class solution:
    def orderlyQueue(self, s: str, k: int) -> str:
        if k == 1:
            answer = s
            ss = s
            for i in range(len(s)):
                temp = ss[1:] + ss[0]
                ss = temp
                answer = min(ss, answer)
            return answer
        else:
            data = {}
            for i, k in enumerate(s):
                if k in data:
                    data[k] += 1
                else:
                    data[k] = 1
            a = sorted(data.items(), key=lambda x: x[0])
            answer = ""
            for k, v in enumerate(a):
                answer += v[0] * v[1]
            return answer

    # def minSubsequence(self, nums: List[int]) -> List[int]:
    #     nums.sort(reverse=True)
    #     tot, s = sum(nums), 0
    #     for i, num in enumerate(nums):
    #         s += num
    #         if s > tot - s:
    #             return nums[:i + 1]

    def addOneRow(
        self, root: Optional[TreeNode], val: int, depth: int
    ) -> Optional[TreeNode]:
        if root.left == None and root.right == None:
            arr = self.marger(root.left, root.right)

    def marger(
        self,
        root: Optional[TreeNode],
        left: Optional[TreeNode],
        right: Optional[TreeNode],
    ):
        arr = []
        if root.left == None and root.right == None:
            return arr.append(root.val)
        else:
            l_arr = self.marger(left, left.left, left.right)
            arr.extend(l_arr)
            r_arr = self.marger(right, right.left, right.right)
            arr.extend(r_arr)
            return arr


def track17api():
    proxies_url = "http://api.shenlongip.com/ip?key=qif1dmqy&pattern=txt&count=1&protocol=1&sign=f7796f6c82db4109ee7d8673fced8554"
    res = requests.get(proxies_url, timeout=5)
    # spider.proxies_time = int(time.time())
    proxies = {
        "http": "http://{}".format(res.text.replace("\r\n", "")),
        "https": "http://{}".format(res.text.replace("\r\n", "")),
    }

    url = "https://apigetway.track718.net/track/real_query_multi"

    payload = json.dumps(
        {
            "tracks": [{"track": "274515026840", "key": "special.fedex.com"}],
            "uuid": "0.9391931341031985-1659680950000",
            "noCache": False,
            "referrer": "https://www.track718.com/zh-CN/detail?nums=274515026840&cb=538###https://www.track718.com/carriers/538-fedex.html",
            "isChoose": True,
            "webDateTime": "2022-08-05 14:29:27",
        }
    )
    headers = {
        "Track718-API-Sign": "92aab510dec035d9e0f400cca2b946f2",
        "Origin": "https://www.track718.com",
        "Referer": "https://www.track718.com/",
        "Host": "apigetway.track718.net",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, proxies=proxies
    )

    print(response.text)


def track123():
    url = "https://www.track123.com/endApi/tk/api/v2/anonymous/track/query-track-nos"

    payload = json.dumps({"logisticsCode": "gls", "trackNos": ["223600646556"]})

    headers = {
        "cookie": "_ga=GA1.2.318421661.1659772754; _gid=GA1.2.979906365.1659772754; _gat_gtag_UA_213536485_2=1",
        "origin": "https://www.track123.com",
        "referer": "https://www.track123.com/result?trackNos=223600646556",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    sum = 0
    for i in range(1000):
        proxies_url = "http://api.shenlongip.com/ip?key=qif1dmqy&pattern=txt&count=1&protocol=1&sign=f7796f6c82db4109ee7d8673fced8554"
        res = requests.get(proxies_url, timeout=5)
        # spider.proxies_time = int(time.time())
        proxies = {
            "http": "http://{}".format(res.text.replace("\r\n", "")),
            "https": "http://{}".format(res.text.replace("\r\n", "")),
        }
        try:
            a1 = time.time()
            a = requests.get(url="https://www.baidu.com/", proxies=proxies, timeout=5)
            a2 = time.time() - a1
            print(a, a2, i, sum)
        except:
            sum += 1
            print(sum)
        pass
