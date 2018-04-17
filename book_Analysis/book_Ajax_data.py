# -*- coding: utf-8 -*-
# @Author: Nessaj
# @Date:   2018-04-11 19:43:59
# @Last Modified by:   Nessaj
# @Last Modified time: 2018-04-17 11:21:13

import requests
from hashlib import md5
import time
import json

# sign: md5(t + public.timestamp + public.pageKey)
pageKey = "aaf50af46621010e7fbeda2b1fe8ef8e"
bookKey = "f2850e634f85f485d719314ae3cfe252"
# sign: md5(page + pagesize + public.timestamp + public.bookKey)
def get_sign(page,pagesize,timestamp,key=bookKey):
    m=md5()
    m.update((str(page)+str(pagesize)+str(timestamp)+key).encode("utf-8"))
    return m.hexdigest()


def get_json(page,pagesize):
    timestamp=int(time.time())
    url="https://ognv1.sqreader.com/index.php?r=pcapi/pcbook/librarysearch"
    sign = get_sign(page,pagesize,timestamp)
    param={
        'page' : page,
        'pageSize' : pagesize,
        'timestamp' : timestamp,
        'sign' : sign,
    }

    response=requests.post(url=url,data=param)
    jsonObj = json.loads(response.text)
    return jsonObj

print(get_json(1,18))

