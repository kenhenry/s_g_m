# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from gm.items import DiscuzItem
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.5194.400 QQBrowser/9.7.13269.400",
    'connection': "keep-alive",}
class DiscuzSpider(scrapy.Spider):
    name = 'gm_s'
    allowed_domains = ['2018guomo.in']
    start_urls = ['http://www.2018guomo.in/archiver/?fid-40.html']  # gm 2,vip 39,rh 36,om 37,tba 38,88s 40
    cookies = {'Ic2x_2132_saltkey': 'i7v1A7zu', 'Ic2x_2132_lastvisit': '1529306547',
              'Hm_lvt_bfd8626bac88fcdca6214c1fa8a5ea54': '1528463003,1528506873,1529215217,1529305549',
              'Hm_lpvt_bfd8626bac88fcdca6214c1fa8a5ea54': '1529310147', 'Ic2x_2132_sendmail': '1',
              'Ic2x_2132_lastact': '1529310173%09member.php%09logging',
              'Ic2x_2132_ulastactivity': '1529310173%7C1',
              'Ic2x_2132_auth': 'c41fitmEtSyCRF9S5tGlX7yyVpxm30eY7bypCN62Pw%2B0KHrIMYCR0WA0fY6VY0i7xIEnIf4zj14xpw00vKLBnuW%2B',
              'Ic2x_2132_lastcheckfeed': '1659%7C1529310173', 'Ic2x_2132_checkfollow': '1',
              'Ic2x_2132_lip': '113.110.141.175%2C1529310173'}


    #  然后获取当前页面内容
    def parse(self, response):
        itemx = []
        for link_s in response.xpath('//*[@id="content"]/ul/li'):
            item = DiscuzItem()

            s_url = link_s.xpath('./a/@href').extract_first()
            item['s_url'] = urljoin(response.url, s_url)
            item['s_url_name'] = link_s.xpath('./a/text()').extract_first()

            itemx.append(item)
            for item in itemx:
                yield scrapy.Request(url=item['s_url'], meta={'item_s': item}, callback=self.parse_d)

        next_page = response.xpath('//*[@id="content"]/div/strong/following-sibling::a[1]/@href').extract_first()
        next_page = urljoin(response.url, next_page)
        if next_page is not None:
            print(next_page)
            yield scrapy.Request(next_page, self.parse)

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

            itemy.append(item)
            for item in itemy:
                # yield scrapy.Request(url=item['detail_url'], meta={'item_d': item}, callback=self.parse_v)
                yield scrapy.Request(url=item['detail_url'], headers=headers, cookies=self.cookies, meta={'item_d': item }, callback=self.parse_v)

# 获取yunfile和keepresource链接

    def parse_v(self, response):
        item = response.meta['item_d']

        item['login_name'] = response.xpath('//*[@id="um"]/p[1]/strong/a/text()').extract_first()
        for link_v in response.xpath( '//td[contains(@id,"postmessage")]/div/div/a'):

            download_url = link_v.xpath('./@href').extract_first()
            item['download_url'] = download_url

            download_url_name = link_v.xpath('./text()').extract_first()
            item['download_url_name'] = download_url_name

            yield item


