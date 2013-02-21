# -*- coding: utf-8 -*-
import os
import bisect
import socket
import struct


def ip2long(ipstr):
        return struct.unpack("!I", socket.inet_aton(ipstr))[0]

region_data = {}
region_data_keys = []
isp_data = {}
isp_data_keys = []
curdir = os.path.dirname(__file__)


def load_region_data(region, file_):
    for line in open(file_):
        arr = line.split()
        if len(arr) != 3:
            continue
        region_data[(ip2long(arr[0]), ip2long(arr[1]))] = region


def load_isp_data(isp, file_):
    for line in open(file_):
        arr = line.split()
        if len(arr) != 2:
            continue
        isp_data[(ip2long(arr[0]), ip2long(arr[1]))] = isp


def init_region_data():
    region_data_dir = os.path.join(curdir, "ipdata", "region")
    for file_ in os.listdir(region_data_dir):
        if not file_.endswith('.txt'):
            continue
        load_region_data(file_.rstrip('.txt'), os.path.join(region_data_dir, file_))
    global region_data_keys
    region_data_keys = sorted(region_data.keys())


def init_isp_data():
    isp_data_dir = os.path.join(curdir, "ipdata", "isp")
    for file_ in os.listdir(isp_data_dir):
        if not file_.endswith('.txt'):
            continue
        load_isp_data(file_.rstrip('.txt'), os.path.join(isp_data_dir, file_))
    global isp_data_keys
    isp_data_keys = sorted(region_data.keys())


def get_region(ip):
    try:
        ip_long = ip2long(ip)
        search_key = (ip_long, ip_long)
        index = bisect.bisect_left(region_data_keys, search_key)
        if index > 0:
            key = region_data_keys[index - 1]
            print "index:%s, key:%s" % (index, key)
            if key[0] <= ip_long < key[1]:
                return region_data[key]
        return "未知"
    except:
        return "未知"


def get_isp(ip):
    try:
        ip_long = ip2long(ip)
        search_key = (ip_long, ip_long)
        index = bisect.bisect_left(isp_data_keys, search_key)
        if index > 0:
            key = isp_data_keys[index - 1]
            print "index:%s, key:%s" % (index, key)
            if key[0] <= ip_long < key[1]:
                return isp_data[key]
        return "未知"
    except:
        return "未知"

init_region_data()
init_isp_data()

if __name__ == "__main__":
    import sys
    print get_region(sys.argv[1])
    print get_isp(sys.argv[1])
