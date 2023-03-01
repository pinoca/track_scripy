from mitmproxy import ctx
import sys
import json
from mitmproxy.http import HTTPFlow


class get_Cookie:
    def request(self, flow: HTTPFlow):
        loaded = """{"data":[{"num":"274515026840","fc":0,"sc":0}],"guid":"","timeZoneOffset":-480}"""
        if flow.request.url == "https://t.17track.net/restapi/track":
            res = flow.request.cookies
            with open("cookies.txt", "w", encoding="utf-8") as f:
                f.write(str(res))
            sys.exit()

    # 所有服务器响应的数据包都会被这个方法处理
    # 所谓的处理，我们这里只是打印一下一些项
    def response(self, flow):
        # 获取响应对象
        response = flow.response


addons = [get_Cookie()]


def parse_cookies(cookie: str) -> dict:
    s = cookie
    list = (", " + s[14:-1]).split("]")
    cookies = {}
    for index, value in enumerate(list[0:-1]):
        cookie = value.replace(", [", "").replace("'", "").replace(" ", "")
        cookies[cookie[: cookie.find(",")]] = cookie[cookie.find(",") + 1 :]
    return cookies


if __name__ == "__main__":
    parse_cookies()
