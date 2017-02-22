# -*- coding: utf-8 -*-
import os
import scrapy
from working_spider.items import OfferItem


class QuotesSpider(scrapy.Spider):
    name = 'pracuj'

    def start_requests(self):
        urls = ['https://www.pracuj.pl/praca/Warszawa;wp/ostatnich%2024h;p,1',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        xpath_offer = '//ul[@id="mainOfferList"]//li[contains(@itemtype, "http://schema.org/JobPosting")]'
        for index, offer in enumerate(response.xpath(xpath_offer), 1):
            yield OfferItem(
                offer_id=offer.xpath('h2').re(r'data-applied-offer-id="(\d+)"')[0],
                job_title=offer.xpath('h2/a/text()').extract_first(),
                job_desc=offer.xpath('div//p[contains(@class, "o-list_item_text_details")]/text()').extract_first(),
                job_loc=offer.xpath('p//span[contains(@class, "o-list_item_desc_location_name_text")]/text()').extract_first(),
                post_date='-',  # TODO: add
                employer=offer.xpath('h3/a/text()').extract_first(),
                offer_link=response.urljoin(offer.xpath('h2/a/@href').extract_first()),
                portal='pracuj.pl'
            )

        # pagination
        next_page = response.xpath('//ul[contains(@class, "desktopPagin")]/li/a[contains(text(), "Następna")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
