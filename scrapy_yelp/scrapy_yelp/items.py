# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyYelpItem(scrapy.Item):
    df = scrapy.Field()

class ScrapyYelpMenuItems(scrapy.Item):
    menuitems= scrapy.Field()


class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
