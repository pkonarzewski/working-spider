# -*- coding: utf-8 -*-
import scrapy


class OfferItem(scrapy.Item):
    offer_id = scrapy.Field()
    job_title = scrapy.Field()
    job_desc = scrapy.Field()
    job_loc = scrapy.Field()
    job_posted = scrapy.Field()
    employeer = scrapy.Field()
    link = scrapy.Field()
    portal = scrapy.Field()
