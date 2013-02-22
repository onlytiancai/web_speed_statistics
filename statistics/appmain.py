# -*- coding: utf-8 -*-

import web
import os
import json
import urlparse

try:
    from . import statistics_helper
except:
    import statistics_helper 

curdir = os.path.dirname(__file__)
render = web.template.render(os.path.join(curdir, 'templates/'))


class index(object):
    def GET(self):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return render.index(statistics_helper.get_clientids())


class statistics(object):
    def GET(self, domain_lookup_time, connect_time, read_content_time):
        referer = web.ctx.env.get('HTTP_REFERER', 'http://undefined.com')
        clientid = urlparse.urlparse(referer).netloc
        web.header('Content-Type', "image/png", unique=True)
        statistics_helper.save_data(clientid, domain_lookup_time, connect_time, read_content_time)
        return ''


class show(object):
    def GET(self, clientid):
        web.header('Content-Type', 'text/html; charset=utf-8', unique=True)
        return render.show({'clientid': clientid})


class statistics_data(object):
    def GET(self, clientid):
        web.header('Content-Type', 'application/json; charset=utf-8', unique=True)
        return json.dumps(statistics_helper.get_data(clientid), indent=4)


urls = ["/", index,
        "/statistics/([^/]+)/([^/]+)/([^/]+).png", statistics,
        "/show/(.*)", show,
        "/statistics_data/(.*)", statistics_data,
        ]

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
