# -*- coding: utf-8 -*-


class OfferFormater(object):

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):

        item['offer_id'] = int(item['offer_id'].strip())
        item['job_title'] = item['job_title'].strip()
        item['job_desc'] = item['job_desc'].strip()
        item['job_loc'] = item['job_loc'].strip()
        item['post_date'] = item['post_date'].strip()
        item['employer'] = item['employer'].strip()
        item['offer_link'] = item['offer_link'].strip()
        item['portal'] = item['portal'].strip()

        return item
