# -*- coding: utf-8 -*-
import os
import re
import logging
import scrapy

from working_spider.items import OfferItem

class OffersSpider(scrapy.Spider):
    name = 'praca'
    current_page = 1

    def start_requests(self):
        urls = ['http://www.praca.pl/s-warszawa_d-1.html?page=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        offers = (response.xpath('//ul[contains(@class, "listing-announcement_new")]')
                  .css('.single-region .announcement-box .announcement-box-table')
                 )

        self.log(response.url, level=logging.INFO)

        index = 0
        for index, offer in enumerate(offers, 1):
            offer_data = offer.css('.announcement-title')
            yield OfferItem(
                offer_id=offer_data.css('.title').xpath('@data-id').extract_first(),
                job_title=offer_data.css('.title::text').extract_first(),
                job_desc=offer_data.css('.title::text').extract_first(),
                job_loc=offer.css('.announcement-area .city::text').extract_first(),
                post_date=offer.css('.announcement-publication-data .data-block::text').extract_first(),
                employer=offer_data.css('.company').xpath('@title').extract_first(),
                offer_link=response.urljoin(offer_data.css('.title').xpath('@href').extract_first()),
                portal="praca.pl"
            )

        if index > 0:
            self.current_page += 1
            self.log('Current page: {}'.format(self.current_page))

            yield scrapy.Request(
                re.sub(r'(\d+)$', str(self.current_page), response.url),
                headers={'X-Requested-With': 'XMLHttpRequest',
                         'Content-Type': 'text/html; charset=UTF-8'},
                callback=self.parse
            )
