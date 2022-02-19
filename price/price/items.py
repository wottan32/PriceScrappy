# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class PriceItem(scrapy.Item):
    # define the fields for your item here like:
    gender = Field()
    productId = Field()
    productName = Field()
    priceOriginal = Field()
    priceSale = Field()

    #items to store links
    imageLink = Field()
    productLink = Field()

    #item for company name
    company = Field()

    pass

    class ImgData(Item):
    #image pipline items to download product images
        image_urls = scrapy.Field()
        images = scrapy.Field()

