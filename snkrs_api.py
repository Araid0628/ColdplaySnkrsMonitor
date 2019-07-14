import requests
import json
import time
import urllib3
from enum import Enum

requests.packages.urllib3.disable_warnings()
# import discord
from skimage import io
# cn = "&country=CN&language=zh-Hans"
# us = "&country=US&language=en"
# jp = "&country=JP&language=ja"
# https://api.nike.com/snkrs/content/v1/?country=CN&language=zh-Hans&offset=0&orderBy=published

# url = "https://api.nike.com/snkrs/content/v1/?country=CN&language=zh-Hans&offset=0&orderBy=published"
# r = json.loads(requests.get(url).text)
# for item in r["threads"]:
#     product = item["product"]
#     engineDict = {
#         "LEO": "LEO(2分钟抽签)",
#         "DAN": "DAN(15分钟抽签)",
#     }
#     try:
#         engine = product["selectionEngine"]
#         status = product["merchStatus"]
#         if "pass" in item["name"]:
#             print("款式: {productName}, 发售时间: {startSellDate}, 发售机制：{selectionEngine}".format(
#                 productName=product["title"], startSellDate=product["startSellDate"],
#                 selectionEngine=engineDict[engine]))
#     except:
#         pass
sneakers = []
ludict = {}
class OrderBy(Enum):
    published = "&orderBy=published"
    updated = "&orderBy=lastUpdated"
url = "https://api.nike.com/snkrs/content/v1/?country=CN&language=zh-Hans"
totalCount = 1000000


def formatTimeStr(time_str):
    return time_str[0:10] + " " + time_str[11:19]


def getTime(time_str):
    return time.mktime(time.strptime(formatTimeStr(time_str), "%Y-%m-%d %H:%M:%S"))


def getLocalTimeStr(time_str):
    tm = getTime(time_str)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tm + 28800)))


def printSneaker(jsonData):
    sneakerInfo = jsonData["name"] + " " + jsonData["title"]
    try:
        if jsonData["product"]["merchStatus"] and not jsonData["restricted"]:
            sneakerInfo += getLocalTimeStr(jsonData["product"]["startSellDate"])
    except:
        pass
    return sneakerInfo


def printSneakerDetail(jsonData):
    selectionEngineDict = {
        "LEO": "LEO(2分钟抽签)",
        "DAN": "DAN(15/30分钟抽签)"
    }
    product = jsonData["product"]
    productInfo = ""
    try:
        productInfo += product["title"]
        if jsonData["restricted"]:
            productInfo += "[受限]"
        if product["publishType"] == "LANUCH":
            engine = product["selectionEngine"]
            publicType = "发售方式" + selectionEngineDict[engine]
        if product["merchStatus"] == "ACTIVE" and product["available"] and "stopSellDate" not in product.keys():
            launchInfo = "发售时间：" + getLocalTimeStr(product["startSellDate"])
        productInfo = publicType + launchInfo
    except:
        pass
    return productInfo


def requestSneakerNoOffset(order):
    global totalCount
    requrl = url + "&offset=0" + order
    http = urllib3.PoolManager()
    r = http.request("GET", requrl)
    shoes = []
    # try:
    json_data = json.loads(r.data)
    if len(sneakers) >= totalCount:
        return []
    totalCount = json_data["totalRecords"]
    for data in json_data["threads"]:
        shoes.append(data["id"])
        ludict[data["id"]] = getTime(data["lastUpdatedDate"])
        # if offset == 0:
        print(printSneaker(data))
    return shoes


def requestSneaker(order, offset):
    # global totalCount
    requrl = url + "&offset=" + str(offset) + order
    http = urllib3.PoolManager()
    r = http.request("GET", requrl)
    shoes = []
    # try:
    json_data = json.loads(r.data)
    # if len(sneakers) >= totalCount:
    #      return []
    # totalCount = json_data["totalRecords"]
    for data in json_data["threads"]:
        shoes.append(data["id"])
        ludict[data["id"]] = getTime(data["lastUpdatedDate"])
        # if offset == 0:
        print(printSneaker(data))
    return shoes
    # except:
        # print("\r访问服务器失败，3秒后重试")
        # time.sleep(3)
       #  return requestSneaker(order, offset)


# for num in range(0, 10000):
#     k = num * 50
#     snkrs = requestSneaker(OrderBy.published.value, k)
#     #snkrs = requestSneakerNoOffset(OrderBy.published.value)
#     if len(snkrs) == 0:
#         print("数据请求完毕,一共获取到", str(len(sneakers)), "条数据(只显示前50条)...")
#         break
#     sneakers.extend(snkrs)



def timer():
    print("Monitoring...")
    while True:
        try:
            http = urllib3.PoolManager()
            requestURL = url + OrderBy.updated.value + "&offset=0"
            r = http.request("GET", requestURL)
            jsonData = json.loads(r.data)
            datas = jsonData["threads"]
        except:
            print("Sleep...")
            time.sleep(10)
            timer()
        for data in datas:
            sneakerid = data["id"]
            t_last_update_date = data["lastUpdateDate"]
            if sneakerid not in sneakers:
                sneakers.append(sneakerid)
                ludict[data["id"]] = getTime(t_last_update_date)
                # await message.channel.send('Hello!')
                printSneakerDetail(data)
        time.sleep(3)


if __name__ == '__main__':
    snkrs = requestSneakerNoOffset(OrderBy.published.value)
    if len(snkrs) == 0:
        print("数据请求完毕")
    sneakers.extend(snkrs)
    timer()
