# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianItem(scrapy.Item):
    title = scrapy.Field()
    auther = scrapy.Field()
    article = scrapy.Field()
    article_id = scrapy.Field()
    time_out = scrapy.Field()
    read_number = scrapy.Field()
    avatar = scrapy.Field()
    meta_title = scrapy.Field()
    meta_description = scrapy.Field()
    meta_keywords = scrapy.Field()
