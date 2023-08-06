# -*- coding:utf-8 -*-
"""
Some commonly used regular expressions.
"""

date = r"(([1-9]\d{3})-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]))"
time = r"((20|21|22|23|[0-1]\d):([0-5]\d):([0-5]\d))"
date_time = r'(%s\s+%s)'%(date, time)
markdown_inserted_image = r'(\!\[([\+\-\w]*)\]\(([\+.\-\w\)\(\/]+)\))'
email = '([A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+)'
url = r'((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)'
server = r'([\w\-_]+(\.[\w\-_]+)+)'
baidu_netdisk_link = r'(链接[:|：](https?://?[a-zA-Z0-9\.\?/=&\s]*)密码[:|：]([a-zA-Z0-9\s]+))'
