# -*- coding: utf-8 -*-

from scrapy import cmdline

name = 'gm_s'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())