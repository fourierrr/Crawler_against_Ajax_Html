# -*- coding: utf-8 -*-
# @Author: Nessaj
# @Date:   2018-04-11 22:33:57
# @Last Modified by:   Nessaj
# @Last Modified time: 2018-04-13 16:17:02


import requests
import re
class pubulishing(object):
    """docstring for pubulishing"""
    def __init__(self,kw,page):

        self.baseurl = 'http://pubs.rsc.org/en/results?searchtext='
        self.kw = kw
        self.api = "http://pubs.rsc.org/en/search/journalresult"
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        self.page = page
    def get_SearchTerm_resultcount(self):

        url = self.baseurl + "{0}".format(self.kw)
        response = requests.get(url=url,headers=self.headers)
        content = response.text
        searchterm = re.search(r'<input id="SearchTerm" name="SearchTerm" type="hidden" value="(.*?)"'
            , content)
        resultcount = re.search(r'{"Type":"all","Count":(\d*?)}',content)
        return searchterm[1],resultcount[1]

    def get_artical_list(self):
        searchterm = self.get_SearchTerm_resultcount()[0]
        param={
            "searchterm" : searchterm,
            "resultcount" : str(self.get_SearchTerm_resultcount()[1]),
            "category" : 'all',
            "pageno" : str(self.page)

        }
        response = requests.post(url=self.api,data=param,headers=self.headers)
        content = response.text
        pat = re.compile(r'<h3 class="capsule__title">\s*(.+?)\s*</h3>')
        artical_list = re.findall(pat,content)
        true_list=[]
        # 文章标题有些格式是用html标签完成的，比如氧气O2的下角标2，这里统一处理掉
        for each in artical_list:
            each = each.replace('<small>','')
            each = each.replace('</small>','')
            each = each.replace('<sub>','')
            each = each.replace('</sub>','')
            each = each.replace('<em>','')
            each = each.replace('</em>','')
            each = true_list.append(each)
        return true_list


pub=pubulishing('bupt',1)

artical_list = pub.get_artical_list()
print(artical_list)