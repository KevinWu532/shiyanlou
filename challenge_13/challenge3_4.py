#!/usr/bin/env python3

import re 
from datetime import datetime

# 使用正则表达式解析日志文件，返回数据列表
def open_parser(filename):
    with open(filename) as logfile:
        # 使用正则表达式解析日志文件
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
                   r'\[(.+)\]\s'  # 时间
                   r'"GET\s(.+)\s\w+/.+"\s'  # 请求路径
                   r'(\d+)\s'  # 状态码
                   r'(\d+)\s'  # 数据大小
                   r'"(.+)"\s'  # 请求头
                   r'"(.+)"'  # 客户端信息
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def max_list(li):
    temp = 0
    for i in li:
        if li.count(i) > temp:
            max_str = i
            temp = li.count(i)
    return {max_str:temp}


def main():

    # 使用正则表达式解析日志文件
    logs = open_parser('/home/shiyanlou/Code/nginx.log')

    '''
    1. 解析文件就是分离不同类型数据（IP，时间，状态码等）
    2. 从解析后的文件中统计挑战需要的信息
    '''
    default = datetime.strptime('2017/1/11', '%Y/%m/%d')
    ip = []
    url = []
    for x in logs:
        date = datetime.strptime(x[1], '%d/%b/%Y:%H:%M:%S +0800')
        if default.date() == date.date():
            ip.append(x[0])
        if x[3] == '404':
            url.append(x[2])
    ip_dict = max_list(ip)
    url_dict = max_list(url)

    return ip_dict, url_dict

if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)
