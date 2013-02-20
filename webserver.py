# -*- coding: utf-8 -*-

import web
import os
import json
from collections import defaultdict

curdir = os.path.dirname(__file__)
render = web.template.render(os.path.join(curdir, 'templates/'))

data_map = defaultdict(web.storage)


class index(object):
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return render.index(json.dumps(data_map, indent=4))


class statistics(object):
    def GET(self, clientid, domain_lookup_time, server_time, read_content_time):
        web.header('Content-Type', "image/png", unique=True)
        data = data_map[clientid]
        
        if 'hits' not in data: data.hits = 0
        if 'domain_lookup_time' not in data: data.domain_lookup_time= 0
        if 'server_time' not in data: data.server_time = 0
        if 'read_content_time' not in data: data.read_content_time= 0

        data.hits += 1 
        data.domain_lookup_time = (data.domain_lookup_time + int(domain_lookup_time)) / 2
        data.server_time= (data.server_time + int(server_time)) / 2
        data.read_content_time= (data.read_content_time + int(read_content_time)) / 2


        return ''


urls = ["/", 'index',
        "/statistics/([^/]+)/([^/]+)/([^/]+)/([^/]+).png", 'statistics',
        ]

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
