# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobOffer(scrapy.Item):
    offer_id = scrapy.Field()
    offer_link = scrapy.Field()
    job_title = scrapy.Field()
    job_desc = scrapy.Field()
    job_loc = scrapy.Field()
    employer_name = scrapy.Field()
    add_date = scrapy.Field()
