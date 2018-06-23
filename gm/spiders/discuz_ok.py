# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from gm.items import DiscuzItem

class DiscuzSpider(scrapy.Spider):
    name = 'discuzok'
    allowed_domains = ['2018guomo.in']
    start_urls = ['http://www.2018guomo.in']

    def parse(self, response):
        item = DiscuzItem()
        achiver_url = response.xpath( '//*[@id="flk"]/p[1]/a[1]/@href').extract_first()
        item['achiver_url'] = urljoin(response.url, achiver_url)
        yield scrapy.Request(url=item['achiver_url'], callback=self.parse_f, meta={'item_a':item})

    def parse_f(self, response):
        item_a = response.meta['item_a']
        items = []
        for link in response.xpath('//*[@id="content"]/ul/li'):
            item = DiscuzItem()
            f_url = link.xpath('./a/@href').extract_first()
            f_url_name = link.xpath('./a/text()').extract_first()
            f_url = urljoin(response.url, f_url)
            item['f_url'] = f_url
            item['f_url_name'] = f_url_name

            item['achiver_url'] = item_a['achiver_url']

            items.append(item)

            for item in items:
                yield scrapy.Request(url=item['f_url'], meta={'item_f': item}, callback=self.parse_s)



    def parse_s(self, response):
        item_f = response.meta['item_f']
        itemx = []
        for link_s in response.xpath('//*[@id="content"]/ul/li'):
            item = DiscuzItem()

            s_url = link_s.xpath('./a/@href').extract_first()
            item['s_url'] = urljoin(response.url, s_url)
            item['s_url_name'] = link_s.xpath('./a/text()').extract_first()

            item['f_url'] = item_f['f_url']
            item['f_url_name'] = item_f['f_url_name']
            item['achiver_url'] = item_f['achiver_url']

            itemx.append(item)
            for item in itemx:
                yield scrapy.Request(url=item['s_url'], meta={'item_s': item}, callback=self.parse_d)

# 最后链接
    def parse_d(self, response):
        item_s = response.meta['item_s']
        itemy = []
        for link_s in response.xpath('//*[@id="end"]/a/@href'):
            item = DiscuzItem()

            detail_url = response.xpath('//*[@id="end"]/a/@href').extract_first()
            item['detail_url'] = urljoin(response.url, detail_url)

            item['s_url'] = item_s['s_url']
            item['s_url_name'] = item_s['s_url_name']
            item['f_url'] = item_s['f_url']
            item['f_url_name'] = item_s['f_url_name']
            item['achiver_url'] = item_s['achiver_url']

            itemy.append(item)
            for item in itemy:
                yield scrapy.Request(url=item['detail_url'], meta={'item_d': item}, callback=self.parse_v)

# 获取yunfile和keepresource链接

    def parse_v(self, response):
        item = response.meta['item_d']
        for link_v in response.xpath( '//td[contains(@id,"postmessage")]/div/a'):

            # '//*[@id="postmessage_842428"]/div/a[1]'
            test_url = link_v.xpath('./@href').extract_first()
            item['test_url'] = urljoin(response.url, test_url)
            yield item


