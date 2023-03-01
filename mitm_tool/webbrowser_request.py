import requests
import random
import os
import json
import webbrowser
import subprocess
import pymongo

# 代理设置
from winproxy import ProxySetting
import time

# 本机IP
locolhost = "127.0.0.1"
# 监听端口
port = "8080"


class bro:
    def __init__(self):
        self.Proxy_set = ProxySetting()
        pass

    def bro_get(self, url: str, file_path: str, file_name: str):
        """
        :param url: 要请求的网站连接
        :param file_path: mitm脚本的文件路径（不包括文件名字）
        :param file_name: mitm脚本的文件名称
        :return:
        """
        # 打开代理
        self.set_proxy(self.Proxy_set)
        # 自动打开网页
        webbrowser.open(url)
        # 打开命令行
        subprocess.check_call("mitmdump -s " + file_name, cwd=file_path)
        time.sleep(8)
        self.close_proxy(self.Proxy_set)
        # 关闭谷歌浏览器
        os.system("taskkill /F /IM chrome.exe")

    def set_proxy(self, Proxy_set):
        """设置系统代理"""
        Proxy_set.enable = True
        Proxy_set.server = locolhost + ":" + port
        Proxy_set.registry_write()

    def close_proxy(self, Proxy_set):
        """关闭系统代理"""
        Proxy_set.enable = False
        Proxy_set.registry_write()


if __name__ == "__main__":
    bo = bro()
    bo.bro_get(
        url="https://t.17track.net/zh-cn?nums=274515026840",
        file_path="D:/Work_Space/scrapy_system/track_spiders/track_spiders/mitm_tool",
        file_name="mitm_track17.py",
    )
