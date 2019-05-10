import requests
import json
import tkinter as tk
import threading
from tkinter import ttk, Frame
import tkinter.filedialog
import re, os
import time
import xlwt
import urllib.parse
import urllib.request
from urllib.parse import urlencode
from tkinter import *

headers = {
    'Host': 'is-hl.snssdk.com',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-A8000 Build/MMB29M) NewsArticle/7.0.3 cronet/TTNetVersion:a729d5c3',
}
#文章链接汇总
urllist= []
#文章评论ID汇总
makelist = []
#评论ID共享链接汇总
gurllist = list(set())
mindex = 1
gindex = 1

data_dict = {}
key_list = []
value_list = []


class xlsmanager():
    def __init__(self, lst):
        self.outwb = xlwt.Workbook()
        self.outws = self.outwb.add_sheet("sheel")
        for v in range(len(lst)):
            self.outws.write(0, v, lst[v])
        self.index = 1

    def add_data(self, lst, name):
        for v in range(len(lst)):
            self.outws.write(self.index, v, str(lst[v]).replace('\n', '').replace('"', '').replace("'", ""))
        self.outwb.save(name)
        self.index += 1


def get_comment(topc_id, start):
    url = "https://mbd.baidu.com/searchbox?" \
          "action=comment" \
          "&cmd=187" \
          "&service=bdbox" \
          "&uid=_82nu_a_S8grav8cj8v080uqBil6iHfggi2T8liH2880a28vga23i_a1v8gAP2tDA" \
          "&from=1014613a&ua=_a-qi4uq-igBNE6lI5me6NN0v8oiaX8DoavjhSdHNqqqB&" \
          "ut=5pXfiNNJ2N_bCvCl_uDehk4Lmq5zA&osname=baiduboxapp&osbranch=a0&" \
          "pkgname=com.baidu.searchbox&" \
          "network=1_0&cfrom=1014613a&" \
          "ctv=2&" \
          "cen=uid_ua_ut&" \
          "typeid=0&" \
          "sid=1013258_4-2054_5102-1013272_2-1578_5389-1013280_6-1013299_2-1013056_2-1013331_2-2142_5349-1013372_3-1013116_2-1013113_3-1919_4717-2178_5436-1012876_4-1012873_1-1167_2514-1013150_1-1013404_1-1013401_3-1946_4803-1013397_1-1013162_3-1013409_1-1013182_1-1007549_23034-1013426_1-1471_3436-1013451_2-1013186_2-1013184_1-1012958_2-1013205_3-1013228_5-1013474_2-1012731_4&" \
          "zid=73BF165EB0BE4937ABC7D7CDA1535C8C61E9A7EC5F698958621A806B972F8F"
    b = {
        "topic_id": topc_id,
        "start": str(start),
        "num": "20",
        "order": "9",
        "source": "feednews",
        # "nid": "news_9515494537961303475"
    }
    data = {
        'data': json.dumps(b),
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '198',
        'Host': 'mbd.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'WISE_HIS_PM=1; fontsize=1.0; BAIDUID=F3A061B43E9EC8DE610074A39AE177E9:FG=1; x-logic-no=5; BAIDULOC=12092176_2483959_40_145_1556166333592; MBD_AT=1556166344; BAIDUCUID=0aSNf0iA28g5avtH0iS6fj8928_6OH8Ng82hugaJ2a87uvt3_PBqi_uHB8_EP2tDA; GID=G1KASJQYLS74862BA5F7A34NTOLJZP1AAS',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    response = requests.post(url=url, data=data, headers=headers)
    data = json.loads(response.text)

    data_list = data["data"]["187"]["list"]
    if data_list == []:
        print("没有评论数据")
        return
    parse_comment(data, topc_id, start)


def parse_comment(data, topc_id, start):
    global mindex
    over = data["data"]["187"]["is_over"]
    data_list = data["data"]["187"]["list"]
    for data in data_list:
        user_name = data['uname']
        datetime = data['create_time']
        datetime = time.localtime(int(datetime))
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", datetime)
        make = [mindex, user_name, datetime]
        add_makedata(make)
        mindex += 1
    if over == False:
        start += 20
        get_comment(topc_id, start)


def check_comment(data, topc_id, start, url, makeid):

    # global gindex
    for key, value in data_dict.items():
        key_list.append(key)
        value_list.append(value)
    if url in value_list:
        get_value_index = value_list.index(url)
        gindex = int(key_list[get_value_index])

    else:
        print("你要查询的值%s不存在" % url)

    data_list = data["data"]["187"]["list"]
    over = data["data"]["187"]["is_over"]
    for data in data_list:
        user_name = data['uname']
        if (user_name == makeid):
            gurl = [gindex, url]
            gurllist.append(gurl)
            gurl_data.insert("", "end", values=(gurl))
            gindex += 1
    if over == False:
        start += 20
        get_comment(topc_id, start)


def get_makeID(makeid):
    global gindex
    gindex = 1
    gurllist.clear()
    clear_tree(gurl_data)
    for v in urllist:
        check_url(v, makeid)


def check_url(url, makeid):
    id = get_urlid(url)
    b = {
        "topic_id": str(id),
        "start": "0",
        "num": "20",
        "order": "9",
        "source": "feednews",
    }
    data = {
        'data': json.dumps(b),
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '198',
        'Host': 'mbd.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'WISE_HIS_PM=1; fontsize=1.0; BAIDUID=F3A061B43E9EC8DE610074A39AE177E9:FG=1; x-logic-no=5; BAIDULOC=12092176_2483959_40_145_1556166333592; MBD_AT=1556166344; BAIDUCUID=0aSNf0iA28g5avtH0iS6fj8928_6OH8Ng82hugaJ2a87uvt3_PBqi_uHB8_EP2tDA; GID=G1KASJQYLS74862BA5F7A34NTOLJZP1AAS',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    comment_url = "https://mbd.baidu.com/searchbox?" \
          "action=comment" \
          "&cmd=187" \
          "&service=bdbox" \
          "&uid=_82nu_a_S8grav8cj8v080uqBil6iHfggi2T8liH2880a28vga23i_a1v8gAP2tDA" \
          "&from=1014613a&ua=_a-qi4uq-igBNE6lI5me6NN0v8oiaX8DoavjhSdHNqqqB&" \
          "ut=5pXfiNNJ2N_bCvCl_uDehk4Lmq5zA&osname=baiduboxapp&osbranch=a0&" \
          "pkgname=com.baidu.searchbox&" \
          "network=1_0&cfrom=1014613a&" \
          "ctv=2&" \
          "cen=uid_ua_ut&" \
          "typeid=0&" \
          "sid=1013258_4-2054_5102-1013272_2-1578_5389-1013280_6-1013299_2-1013056_2-1013331_2-2142_5349-1013372_3-1013116_2-1013113_3-1919_4717-2178_5436-1012876_4-1012873_1-1167_2514-1013150_1-1013404_1-1013401_3-1946_4803-1013397_1-1013162_3-1013409_1-1013182_1-1007549_23034-1013426_1-1471_3436-1013451_2-1013186_2-1013184_1-1012958_2-1013205_3-1013228_5-1013474_2-1012731_4&" \
          "zid=73BF165EB0BE4937ABC7D7CDA1535C8C61E9A7EC5F698958621A806B972F8F"
    response = requests.post(url=comment_url, data=data, headers=headers)
    data = json.loads(response.text)

    data_list = data["data"]["187"]["list"]
    if data_list == []:
        print("没有评论数据")
        return
    check_comment(data, id, 0, url, makeid)


def get_re(id, topc_id, start):
    lst = ["ID", "时间"]
    xls = xlsmanager(lst)
    url = "https://mbd.baidu.com/searchbox?" \
          "action=comment" \
          "&cmd=187" \
          "&service=bdbox" \
          "&uid=_82nu_a_S8grav8cj8v080uqBil6iHfggi2T8liH2880a28vga23i_a1v8gAP2tDA" \
          "&from=1014613a&ua=_a-qi4uq-igBNE6lI5me6NN0v8oiaX8DoavjhSdHNqqqB&" \
          "ut=5pXfiNNJ2N_bCvCl_uDehk4Lmq5zA&osname=baiduboxapp&osbranch=a0&" \
          "pkgname=com.baidu.searchbox&" \
          "network=1_0&cfrom=1014613a&" \
          "ctv=2&" \
          "cen=uid_ua_ut&" \
          "typeid=0&" \
          "sid=1013258_4-2054_5102-1013272_2-1578_5389-1013280_6-1013299_2-1013056_2-1013331_2-2142_5349-1013372_3-1013116_2-1013113_3-1919_4717-2178_5436-1012876_4-1012873_1-1167_2514-1013150_1-1013404_1-1013401_3-1946_4803-1013397_1-1013162_3-1013409_1-1013182_1-1007549_23034-1013426_1-1471_3436-1013451_2-1013186_2-1013184_1-1012958_2-1013205_3-1013228_5-1013474_2-1012731_4&" \
          "zid=73BF165EB0BE4937ABC7D7CDA1535C8C61E9A7EC5F698958621A806B972F8F"
    b = {
        "topic_id": topc_id,
        "start": str(start),
        "num": "20",
        "order": "9",
        "source": "feednews",
    }
    data = {
        'data': json.dumps(b),
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '198',
        'Host': 'mbd.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'WISE_HIS_PM=1; fontsize=1.0; BAIDUID=F3A061B43E9EC8DE610074A39AE177E9:FG=1; x-logic-no=5; BAIDULOC=12092176_2483959_40_145_1556166333592; MBD_AT=1556166344; BAIDUCUID=0aSNf0iA28g5avtH0iS6fj8928_6OH8Ng82hugaJ2a87uvt3_PBqi_uHB8_EP2tDA; GID=G1KASJQYLS74862BA5F7A34NTOLJZP1AAS',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    response = requests.post(url=url, data=data, headers=headers)
    data = json.loads(response.text)

    data_list = data["data"]["187"]["list"]
    if data_list == []:
        print("没有评论数据")
        return
    parse_re(id, data, topc_id, start, xls)


def parse_re(id, data, topc_id,  start, xls):
    over = data["data"]["187"]["is_over"]
    data_list = data["data"]["187"]["list"]
    for data in data_list:
        user_name = data['uname']
        datetime = data['create_time']
        datetime = time.localtime(int(datetime))
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", datetime)
        make = [user_name, topc_id, datetime]
        path = id + ".xls"
        xls.add_data(make, path)
    if over == False:
        start += 20
        get_re(id, topc_id, start)


def start_collection(url):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '198',
        'Host': 'mbd.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'WISE_HIS_PM=1; fontsize=1.0; BAIDUID=F3A061B43E9EC8DE610074A39AE177E9:FG=1; x-logic-no=5; BAIDULOC=12092176_2483959_40_145_1556166333592; MBD_AT=1556166344; BAIDUCUID=0aSNf0iA28g5avtH0iS6fj8928_6OH8Ng82hugaJ2a87uvt3_PBqi_uHB8_EP2tDA; GID=G1KASJQYLS74862BA5F7A34NTOLJZP1AAS',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    # global urllist
    # count = len(urllist)+1
    # response = requests.get(url, headers=headers)
    # url = response.url
    # urllist.append(url)
    # url_data.insert("", "end", values=(count, url))
    # topc_id = get_urlid(url)
    # get_re(topc_id, 0)

    global urllist
    values = url.split(',')
    id = values[0]
    url = values[1]
    # print(url)
    # response = requests.get(url, headers=headers)
    # url = response.url
    # print('123', url)
    urllist.append(url)
    # url_data.insert("", "end", values=(id, url))
    item_id = get_urlid(url)
    get_re(id, item_id, start=0)
    data_dict[id] = url
    for key, value in data_dict.items():
        url_data.insert('', key, values=(key, value))


def get_urlid(url):
    news_id = ''.join(re.compile(r"news_(\d+)", re.S).findall(url))
    url_un = "https://mbd.baidu.com/newspage/api/landing?cmd=103&refresh=4&wfr=&page=landingreact&context=%7B%22nid%22%3A%22news_{}%22%7D&service=bdbox&uid=giHdu08Zv8g4aH88Y82E808CSa0tivi7_i2mulu0vu8jav8_ju2N8_ag2igAa2t1A&from=1001128e&ua=_avLC_aE-i4qywoUfpw1z4uS2N_-h2N4_uL5ixLqA&ut=pyAt69RQ2CyjaXiDouD58gIVLqNRpmq6A&osname=baiduboxapp&osbranch=a0&pkgname=com.baidu.searchbox&network=1_0&cfrom=1001128e&ctv=2&cen=uid_ua_ut&typeid=0&sid=1013260_1-2054_5103-1562_3682-1013294_2-1578_5389-1013280_1-1074_2311-1013308_1-1013325_1-2118_5590-1013317_1-588_1201-2126_5286-2127_5288-2131_5582-1013335_1-1013357_5-2148_5362-1013351_2-1013375_3-2164_5392-2165_5395-2171_5414-2172_5419-2175_5425-2182_5447-2188_5458-1013378_1-2190_5461-2191_5464-1167_2514-1013401_2-1176_2541-1690_4807-1013396_1-1013395_15-1013393_2-2211_5531-1013411_2-1013427_4-1726_4065-1013455_4-1013452_1-1012958_1-1751_4130-1759_4149-1013482_2-1789_5139-1813_4378-1819_4393-1831_4420-1840_4442-1013040_3-1013071_2-1013056_2-1886_4558-1013103_1-1903_4607-1906_4626-1013114_3-1919_4716-1932_4773-1934_4778-1013150_2-1013149_1-1946_4803-1962_4834-1013182_1-1007549_23033-1471_3435-1013185_1-1012698_1-2025_5029-1013239_3-1013238_3-1013233_2&zid=C6F27B4AE2B571FDF21A538D612489A0C1DAD37FDC75A31FC2F417D3646D2C".format(
        news_id)
    url = urllib.request.unquote(url_un)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '198',
        'Host': 'mbd.baidu.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'WISE_HIS_PM=1; fontsize=1.0; BAIDUID=F3A061B43E9EC8DE610074A39AE177E9:FG=1; x-logic-no=5; BAIDULOC=12092176_2483959_40_145_1556166333592; MBD_AT=1556166344; BAIDUCUID=0aSNf0iA28g5avtH0iS6fj8928_6OH8Ng82hugaJ2a87uvt3_PBqi_uHB8_EP2tDA; GID=G1KASJQYLS74862BA5F7A34NTOLJZP1AAS',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    d = {
        'url': url_un,
    }
    data = {
        'data': json.dumps(d)
    }
    response = requests.get(url, data=data, headers=headers, verify=False)
    json_data = json.loads(response.text)

    intent = json_data['data']['pageInfo']['common']['favorite']['cmd']
    json_intent = json.loads(intent)
    intent = json_intent['intent']
    intent = urllib.request.unquote(intent)
    topc_id = ''.join(re.compile(r"""intent:#Intent;S\.commentInfo={"topic_id":"(\d+)",.*?;""", re.S).findall(intent))
    return topc_id


def get_url(url):
    global mindex
    mindex = 1
    id = get_urlid(url)
    clear_tree(make_data)
    makelist.clear()
    get_comment(id, 0)


def datetime_str(timer):
    timeArray = time.localtime(timer)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def clear_tree(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


def add_makedata(lst):
    makelist.append(lst)
    make_data.insert("","end",values=(lst))


def import_urls():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    }
    global urllist
    selectFileName = tkinter.filedialog.askopenfilename(title="选择文件", filetypes=[('Text file', '*.txt')])
    if(selectFileName != ""):
        with open(selectFileName, "r") as f:
            for li in f.readlines():
                print(li)
                values = li.split(',')
                id = values[0]
                url = values[1]
                # response = requests.get(url, headers=headers)
                # url = response.url
                urllist.append(url)
                topc_id = get_urlid(url)
                get_re(id, topc_id, 0)
                data_dict[id] = url
        print(data_dict)
        clear_tree(url_data)
        for key, value in data_dict.items():
            url_data.insert('', key, values=(key, value))


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()
    # t.join()


def urltreeviewClick(event):
    if len(url_data.selection()) > 0:
        item = url_data.selection()[0]
        url = url_data.item(item, "values")[1]
        get_url(url)


def maketreeviewClick(event):
    if len(make_data.selection()) > 0:
        item = make_data.selection()[0]
        make = make_data.item(item, "values")[1]
        get_makeID(make)


def gurltreeviewClick(event):
    if len(url_data.selection()) > 0:
        item = url_data.selection()[0]
        url = url_data.item(item, "values")[1]
        print(url)


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    print(tv.get_children(''))
    l.sort(reverse=reverse)  # 排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # 根据排序后索引移动
        tv.move(k, '', index)
        print(k)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def clear_alldata():
    # clear_tree(make_data)
    # clear_tree(url_data)
    # clear_tree(gurl_data)
    # makelist.clear()
    # urllist.clear()
    # gurllist.clear()

    for url in urllist:
        # urlid = get_urlid(url)
        for key, value in data_dict.items():
            key_list.append(key)
            value_list.append(value)
        if url in value_list:
            get_value_index = value_list.index(url)
            gindex = key_list[get_value_index]
            filename = gindex+'.xls'
            os.remove(filename)
    clear_tree(make_data)
    clear_tree(url_data)
    clear_tree(gurl_data)
    makelist.clear()
    urllist.clear()
    gurllist.clear()


def export_data():
    # if len(url_data.selection()) > 0:
    #     lst = ["编号", "ID", "时间"]
    #     xlsx = xlsmanager(lst)
    #     item = url_data.selection()[0]
    #     path = get_urlid(url_data.item(item, "values")[1]) + ".xls"
    #     for v in makelist:
    #         xlsx.add_data(v, path)

    if len(url_data.selection()) > 0:
        lst = ["编号", "ID", "时间"]
        xlsx = xlsmanager(lst)
        item = url_data.selection()[0]
        # url = url_data.item(item, "values")[1]
        # path = get_urlid(url_data.item(item, "values")[1]) + ".xls"
        # print('123456', path)
        id = get_urlid(url_data.item(item, "values")[1])
        url = url_data.item(item, "values")[1]
        for key, value in data_dict.items():
            key_list.append(key)
            value_list.append(value)
        if url in value_list:
            get_value_index = value_list.index(url)
            gindex = key_list[get_value_index]
            path = gindex + '__' + id + ".xls"
        for v in makelist:
            xlsx.add_data(v, path)


def export_data1():
    # if len(make_data.selection()) > 0:
    #     item = make_data.selection()[0]
    #     make = make_data.item(item, "values")[1]
    #     lst = ["编号", "共享链接"]
    #     xlsx = xlsmanager(lst)
    #     item = url_data.selection()[0]
    #     path = make + ".xls"
    #     for v in gurllist:
    #         xlsx.add_data(v, path)

    if len(make_data.selection()) > 0:
        item = make_data.selection()[0]
        make = make_data.item(item, "values")[1]
        lst = ["编号", "共享链接"]
        xlsx = xlsmanager(lst)
        item = url_data.selection()[0]
        path = make + ".xls"
        for v in gurllist:
            xlsx.add_data(v, path)


def delete_info1():

    item = url_data.selection()[0]
    url = url_data.item(item, "values")[1]
    print('haha', url)
    # url_data.delete(item)
    for key, value in data_dict.items():
        key_list.append(key)
        value_list.append(value)
    if url in value_list:
        get_value_index = value_list.index(url)
        gindex = key_list[get_value_index]
        filename = gindex + '.xls'
        print(filename)
        os.remove(filename)
    Button(window,

               command=url_data.delete(item)
               )


def delete_info2():
    item = make_data.selection()[0]
    # url_data.delete(item)
    Button(window,

           command=make_data.delete(item)
           )
    id = get_urlid(url_data.item(item, "values")[1])
    url = url_data.item(item, "values")[1]
    for key, value in data_dict.items():
        key_list.append(key)
        value_list.append(value)
    if url in value_list:
        get_value_index = value_list.index(url)
        gindex = key_list[get_value_index]
        path = gindex + '__' + id + ".xls"
        os.remove(path)


def delete_info3():
    global gurl_data
    item = gurl_data.selection()[0]
    Button(window,
           command=gurl_data.delete(item)
    )


if __name__ == '__main__':
    window = tk.Tk()
    window.title('百度app分析工具')
    window.geometry('700x800+700+150')
    window.resizable(False, False)
    tk.Label(window, text="文章链接:").place(x=20, y=20)
    title = tk.StringVar()
    title.set("")
    entry_usr_name = tk.Entry(window, textvariable=title, width=50)
    entry_usr_name.place(x=80, y=20)
    btn_collect = tk.Button(window, text='导入', command=lambda: thread_it(start_collection, title.get()), width=6,
                            height=1)
    btn_collect.place(x=440, y=12)
    btn_import = tk.Button(window, text='批量导入', command=lambda: thread_it(import_urls), width=8, height=1)
    btn_import.place(x=500, y=12)
    btn_alldel = tk.Button(window, text='清空数据', command=clear_alldata, width=8, height=1)
    btn_alldel.place(x=580, y=12)

    btn_export1 = tk.Button(window, text='删除数据', command=delete_info1, width=8, height=1)
    btn_export1.place(x=580, y=120)

    btn_export = tk.Button(window, text='导出数据', command=export_data, width=8, height=1)
    btn_export.place(x=580, y=320)

    btn_export1 = tk.Button(window, text='删除数据', command=delete_info2, width=8, height=1)
    btn_export1.place(x=580, y=400)

    btn_export1 = tk.Button(window, text='导出数据', command=export_data1, width=8, height=1)
    btn_export1.place(x=580, y=520)

    btn_export1 = tk.Button(window, text='删除数据', command=delete_info3, width=8, height=1)
    btn_export1.place(x=580, y=600)

    urlframe = Frame(window)
    urlframe.place(x=70, y=50, width=480, height=200)
    scrollBar = tkinter.Scrollbar(urlframe)
    scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    url_data = ttk.Treeview(urlframe, show="headings", yscrollcommand=scrollBar.set)
    url_data['columns'] = ['index', 'url']
    url_data.column('index', width=50, anchor='center')
    url_data.column('url', width=400, anchor='center')
    url_data.heading('index', text='编号')
    url_data.heading('url', text='链接')
    url_data.bind("<ButtonRelease-1>", urltreeviewClick)
    # url_data.bind("<ButtonRelease-1>", urldeleteviewClick)
    url_data.pack(side=tkinter.LEFT, fill=tkinter.Y)
    scrollBar.config(command=url_data.yview)



    tk.Label(window, text="文章评论ID汇总:").place(x=70, y=250)
    dataframe = Frame(window)
    dataframe.place(x=70, y=270, width=480, height=200)
    scrollBar1 = tkinter.Scrollbar(dataframe)
    scrollBar1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    make_data = ttk.Treeview(dataframe, show="headings", yscrollcommand=scrollBar1.set)
    make_data['columns'] = ['index', 'name', "datetime"]
    make_data.column('index', width=50, anchor='center')
    make_data.column('name', width=200, anchor='center')
    make_data.column('datetime', width=200, anchor='center')
    make_data.heading('name', text='ID')
    make_data.heading('index', text='编号')
    make_data.heading('datetime', text='时间', command=lambda: treeview_sort_column(make_data, 'datetime', False))
    make_data.bind('<ButtonRelease-1>', maketreeviewClick)
    make_data.pack(side=tkinter.LEFT, fill=tkinter.Y)
    scrollBar1.config(command=make_data.yview)

    tk.Label(window, text="评论ID文章链接汇总:").place(x=70, y=470)
    gurlframe = Frame(window)
    gurlframe.place(x=70, y=490, width=480, height=200)
    gscrollBar = tkinter.Scrollbar(gurlframe)
    gscrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    gurl_data = ttk.Treeview(gurlframe, show="headings", yscrollcommand=gscrollBar.set)
    gurl_data['columns'] = ['index', 'url']
    gurl_data.column('index', width=50, anchor='center')
    gurl_data.column('url', width=400, anchor='center')
    gurl_data.heading('index', text='编号')
    gurl_data.heading('url', text='链接')
    gurl_data.bind("<ButtonRelease-1>", gurltreeviewClick)
    gurl_data.pack(side=tkinter.LEFT, fill=tkinter.Y)
    gscrollBar.config(command=gurl_data.yview)




    window.mainloop()