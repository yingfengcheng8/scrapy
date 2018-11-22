# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item,Field


class CsdbItem(Item):
    # define the fields for your item here like:
    formula = Field()
    name = Field()
    category = Field()
    information = Field()
    Reference = Field()
    Hydrogen_storage = Field()
    optimum_Hydrogen_storage = Field()
    method = Field()
    image = Field()
