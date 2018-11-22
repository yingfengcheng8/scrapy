# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IbondItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    Structure = scrapy.Field()
    Solvent = scrapy.Field()
    solvent_full_name = scrapy.Field()
    pKa = scrapy.Field()
    Method = scrapy.Field()
    method_description = scrapy.Field()
    Ref = scrapy.Field()
    ref_content = scrapy.Field()
    doi = scrapy.Field()


