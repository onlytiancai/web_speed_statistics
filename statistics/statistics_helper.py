# -*- coding: utf-8 -*-

import web
from collections import defaultdict

try:
    from . import iphelper
except:
    import iphelper

region_data_map = defaultdict(dict)
isp_data_map = defaultdict(dict)

region_map = {
    "香港": "HKG",
    "海南": "HAI",
    "云南": "YUN",
    "北京": "BEI",
    "天津": "TAJ",
    "新疆": "XIN",
    "西藏": "TIB",
    "青海": "QIH",
    "甘肃": "GAN",
    "内蒙古": "NMG",
    "宁夏": "NXA",
    "山西": "SHX",
    "辽宁": "LIA",
    "吉林": "JIL",
    "黑龙江": "HLJ",
    "河北": "HEB",
    "山东": "SHD",
    "河南": "HEN",
    "陕西": "SHA",
    "四川": "SCH",
    "重庆": "CHQ",
    "湖北": "HUB",
    "安徽": "ANH",
    "江苏": "JSU",
    "上海": "SHH",
    "浙江": "ZHJ",
    "福建": "FUJ",
    "台湾": "TAI",
    "江西": "JXI",
    "湖南": "HUN",
    "贵州": "GUI",
    "广西": "GXI",
    "广东": "GUD",
}


def set_statistics_data(data, domain_lookup_time, connect_time, read_content_time):
    if 'hits' not in data: data.hits = 0
    if 'domain_lookup_time' not in data: data.domain_lookup_time = 0
    if 'connect_time' not in data: data.connect_time = 0
    if 'read_content_time' not in data: data.read_content_time = 0
    if 'response_time' not in data: data.response_time = 0

    data.hits += 1
    data.domain_lookup_time = (data.domain_lookup_time + int(domain_lookup_time)) / 2
    data.connect_time = (data.connect_time + int(connect_time)) / 2
    data.read_content_time = (data.read_content_time + int(read_content_time)) / 2
    data.response_time = (data.response_time + int(domain_lookup_time) + int(connect_time) + int(read_content_time)) / 2


def save_data(clientid, domain_lookup_time, connect_time, read_content_time):
    ip = web.ctx.ip
    region = iphelper.get_region(ip)
    isp = iphelper.get_isp(ip)

    data = region_data_map[clientid]
    if region not in data:
        data[region] = web.storage()
    data = data[region]
    set_statistics_data(data, domain_lookup_time, connect_time, read_content_time)

    data = isp_data_map[clientid]
    if isp not in data:
        data[isp] = web.storage()
    data = data[isp]
    set_statistics_data(data, domain_lookup_time, connect_time, read_content_time)


def clear_data():
    region_data_map.clear()
    isp_data_map.clear()


def get_data(clientid):
    result = defaultdict(list)

    data = region_data_map[clientid]
    for region in data:
        region_data = data[region].copy()
        region_data['cha'] = region_map.get(region, 'TAI')  # 找不到算台湾的
        region_data['name'] = region
        result['region_data'].append(region_data)

    data = isp_data_map[clientid]
    for isp in data:
        isp_data = data[region].copy()
        isp_data['name'] = isp
        result['isp_data'].append(isp_data)

    return result


def get_clientids():
    return sorted(region_data_map.keys())
