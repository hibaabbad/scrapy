# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OthersitesItem(scrapy.Item):
   url = scrapy.Field()
   name = scrapy.Field()
   price = scrapy.Field()
   photo = scrapy.Field()
   description = scrapy.Field()
   type = scrapy.Field()
   disque = scrapy.Field()
   ram = scrapy.Field()
   cpu = scrapy.Field()
   marque = scrapy.Field()
   ecran = scrapy.Field()
