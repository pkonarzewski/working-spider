# -*- coding: utf-8 -*-
import os
import re
import logging
import scrapy

from working_spider.items import OfferItem

class OffersSpider(scrapy.Spider):
    name = 'monster'
    total_pages = None

    def start_requests(self):
        urls = ['https://www.monsterpolska.pl/praca/q/?where=Warszawa%2C%20mazowieckie&tm=0&cy=pl&page=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.total_pages is None:
            self.total_pages = int(response.xpath('//input[contains(@id, "totalPages")]/@value').extract_first())
            self.log('TotalPages: {}'.format(self.total_pages), level=logging.INFO)

        current_page = int(response.xpath('//input[contains(@id, "currentPage")]/@value').extract_first())
        self.log('CurrentPage: {}'.format(current_page), level=logging.INFO)

        offers = response.xpath('//div/article[contains(@itemtype, "https://schema.org/JobPosting")]')
        for index, offer in enumerate(offers, 1):
            yield OfferItem(
                offer_id=offer.xpath('div[contains(@class, "jobTitle")]/h2/a/@data-m_impr_j_jobid').extract_first(),
                job_title=offer.xpath('div[contains(@class, "jobTitle")]/h2/a/span/text()').extract_first(),
                job_desc=offer.xpath('meta[contains(@itemprop, "description")]/@content').extract_first(),
                job_loc=offer.xpath('div[contains(@class, "location")]/span[contains(@itemprop, "name")]/text()').extract_first(),
                post_date=offer.xpath('div[contains(@class, "extras")]/div/time/@datetime').extract_first(),
                employer=offer.xpath('div[contains(@class, "company")]/a/span/text()').extract_first(),
                offer_link=offer.xpath('div[contains(@class, "jobTitle")]/h2/a/@href').extract_first(),
                portal="Monster.pl"
            )
        if current_page < self.total_pages:
            next_page = re.sub(r'(\d+)$', str(current_page+1), response.url)
            yield scrapy.Request(next_page, callback=self.parse)
