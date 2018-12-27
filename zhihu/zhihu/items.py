# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 热榜页面信息
    # 问题
    question = Field()
    # 热度
    question_heat = Field()
    content = Field()
    video = Field()
    image = Field()
    answer_name = Field()
    answer_token = Field()