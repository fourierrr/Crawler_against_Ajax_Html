# -*- coding: utf-8 -*-
# @Author: Nessaj
# @Date:   2018-04-11 15:12:33
# @Last Modified by:   Nessaj
# @Last Modified time: 2018-04-22 15:19:09

"参考文章https://cuiqingcai.com/5024.html"

import execjs
import os
# import execjs.runtime_names
import requests
# os.environ["EXECJS_RUNTIME"] = "Node"
# print(execjs.get().name)
# Init environment
node = execjs.get(execjs.runtime_names.Node)

# Params
method = 'GETCITYWEATHER'
city = '北京'
stype = 'HOUR'
start_time = '2018-01-25 00:00:00'
end_time = '2018-01-25 23:00:00'

# Compile javascript
file = 'weather_encryption.js'

ctx = execjs.compile(open(file,'r',encoding="utf-8").read())

# Get params
js = 'getEncryptedData("{0}", "{1}", "{2}", "{3}", "{4}")'.format(method, city, stype, start_time, end_time)

params = ctx.eval(js)

# Get encrypted response text
api = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
response = requests.post(api, data={'d': params})

#原网页的接口服务器返回的数据出了一点问题，返回的数据多了一些warning，replace就行
text=response.text.replace('''<br />
<b>Warning</b>:  mysqli_connect(): Headers and client library minor version mismatch. Headers:50556 Library:50637 in <b>/var/www/aqistudy/config/db_config.php</b> on line <b>39</b><br />''','')
text=text.replace(' ','')
text=text.replace('\n','')

# Decode data
# js1 = 'decodeData("{0}")'.format(response.text)

js = 'decodeData("{0}")'.format(text)
decrypted_data = ctx.eval(js)
print(decrypted_data)