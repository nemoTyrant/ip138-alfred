# !/usr/bin/python
# encoding: utf-8

import sys
import re
from bs4 import BeautifulSoup, element
from workflow import Workflow, web


# get data from web
def get_data(query):
    url = "http://www.ip138.com/ips138.asp?ip=" + query
    res = web.get(url)
    if(res.status_code != 200):
        return [{"title": u"网页无法打开"}]
    else:
        data = []
        res = BeautifulSoup(res.text, "html.parser").findAll("table")[2]
        ip = res.h1.string
        match = re.search("(?<=[\s:])(\d+\.){3}\d+$", ip)
        if match:
            data.append({"title": ip, "arg": match.group()})
        else:
            data.append({"title": u"无效的域名或IP"})

        if res.ul:
            for li in res.ul:
                data.append({"title": li.string, "arg": li.string})
        return data


def get_results(wf, query):
    data = wf.cached_data(query, max_age = 86400 * 10)
    # data = wf.cached_data(query, max_age = 1)
    if data is None:
        data = get_data(query)
        wf.cache_data(query, data)
    for line in data:
        if line.get("arg"):
            wf.add_item(line["title"], valid=True, arg=line["arg"])
        else:
            wf.add_item(line["title"])


def main(wf):
    args = wf.args

    if len(args) < 1:
        wf.add_item(u'请输入查询域名或IP')
    else:
        get_results(wf, args[0].strip())
    wf.send_feedback();
    

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
