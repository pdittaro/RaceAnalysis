# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RaceResult(scrapy.Item):

    race = scrapy.Field()
    series = scrapy.Field()
    category = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    filename = scrapy.Field()
