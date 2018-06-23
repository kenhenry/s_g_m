# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiscuzItem(scrapy.Item):
    # define the fields for your item here like:
    # achiver_url = scrapy.Field()
    #
    # next_page_name = scrapy.Field()
    #
    # f_url = scrapy.Field()
    # f_url_name = scrapy.Field()

    s_url = scrapy.Field()
    s_url_name = scrapy.Field()

    detail_url = scrapy.Field()

    # yunfile_url = scrapy.Field()
    # yunfile_url_name = scrapy.Field()
    #
    # keepresource_url = scrapy.Field()
    # keepresource_url_name = scrapy.Field()

    download_url = scrapy.Field()
    download_url_name = scrapy.Field()

    login_name = scrapy.Field()




    pass
