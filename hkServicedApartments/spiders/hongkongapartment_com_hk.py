# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from hkServicedApartments.items import hkServicedApartmentsItem

class hongkongApartmentsSpider(CrawlSpider):
    name = "hongkongapartment.com.hk"
    allowed_domains = ["hongkongapartment.com.hk"]
    start_urls = [
        "http://hongkongapartment.com.hk/search/category/mapormtr/map/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//div[@class="nav-previous"]/a',)), callback="parse_items", follow=True),
    )

    def parse_items(self, response):
        for sel in response.xpath('//h2[@class="entry-title-list"]/a'):
            item = hkServicedApartmentsItem()
            item['name'] = sel.xpath('text()').extract()[0].encode('utf-8')
            item['link'] = sel.xpath('@href').extract()[0]
            request = scrapy.Request(item['link'], callback=self.parse_apartment)
            request.meta['item'] = item
            yield request

    def parse_apartment(self, response):
        item = response.meta['item']
        #log.msg("Parsing apartment " + item['name'])
        item['price'] = response.xpath('//div[@class="detailPrice"]/span/text()').extract()
        for row in response.xpath('//div[@class="detailTxt"]/table/tr'):
            rowtitle = row.xpath('td[@class="detailTxt-title"]/text()').extract()
            rowtitle = rowtitle[0].encode('utf-8')
            if rowtitle == '住所':
                item['address'] = row.xpath('td/text()')[2].extract().strip()
        return item


