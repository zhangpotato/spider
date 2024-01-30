# -*-coding:utf-8-*-
import time

import requests
from bs4 import BeautifulSoup


def get_url(url):
    return url[0:url.rindex("/") + 1]


def get_html(url):
    while True:
        try:
            response = requests.get(url, timeout=10)
            response.encoding = "utf-8"
            if response.status_code == 200:
                return BeautifulSoup(response.text, "lxml")
            else:
                time.sleep(5)
                continue
        except Exception:
            continue


def spider(url, level):
    base_url = get_url(url)
    if level == 1:
        tr_class = "tr.provincetr"
    elif level == 2:
        tr_class = "tr.citytr"
    elif level == 3:
        tr_class = "tr.countytr"
    elif level == 4:
        tr_class = "tr.towntr"
    else:
        tr_class = "tr.villagetr"
    time.sleep(1)
    for item_tr in get_html(url).select(tr_class):

        item_td = item_tr.select("td")
        area_code = item_td[0].select_one("a")
        # 判断是否是街道级别，街道级别的无法通过select_one("a")获取内容
        if area_code is None:
            area_code = item_td[0].text
            area_name = item_td[1].text
            if level > 4:
                area_name = item_td[2].text
            print(area_code + "\t" + area_name)
            # 写入到文件
            file.write(area_code + "\t" + area_name + "\n")
        else:
            # 判断区域码值是否为数字，如果是数字则表示为区域码值，否则表示为省份
            if area_code.text.isnumeric():
                area_href = item_td[0].select_one("a").get("href")
                # 判断是否有网址链接，有网址链接则获取链接，没有链接的则只取码值和区域名称
                if area_href is None:
                    print("当前区域的链接为空")
                    area_code = item_td[0].select_one("a").text
                    area_name = item_td[1].select_one("a").text
                    print(area_code + "\t" + area_name)
                    # 写入到文件
                    file.write(area_code + "\t" + area_name + "\n")
                # 链接不为空，则获取下一级别的码值
                else:
                    area_code = item_td[0].select_one("a").text
                    area_name = item_td[1].select_one("a").text
                    url = base_url + area_href

                    print(area_code + "\t" + area_name + "\t" + url)
                    # 写入到文件
                    file.write(area_code + "\t" + area_name+"\n")
                    spider(url, level + 1)
            else:
                # 没有码值，则该层级是省份 ，只获取省份名称及网址
                for province in item_td:
                    area_name = province.text
                    url = base_url + province.select_one("a").get("href")
                    print(area_name + "\t" + url)
                    # base_url = get_url(url)

                    spider(url, level + 1)


# 入口
if __name__ == '__main__':
    url = 'https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html'
    file = open("area-code-2023.txt", "w", encoding="utf-8")
    spider(url, 1)
    file.close()
