# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
结构定义

'''


class ScrapyDongmanDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # 套图标题
    title = scrapy.Field()
    # 套图详情页标题
    detail_title = scrapy.Field()
    # 套图地址
    url = scrapy.Field()
    # 详细页地址
    pic_url = scrapy.Field()
    # 详细页图片下载地址
    down_path = scrapy.Field()
