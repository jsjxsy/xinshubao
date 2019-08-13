# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XinshubaoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    story_image_url = scrapy.Field()
    lasted_update = scrapy.Field()
    story_status = scrapy.Field()
    story_description = scrapy.Field()
    pass


class StoryContent(scrapy.Item):
    story_chapter = scrapy.Field()
    story_chapter_url = scrapy.Field()
    pass


class StoryChapterContent(scrapy.Item):
    story_name = scrapy.Field()
    story_chapter_name = scrapy.Field()
    story_chapter_content = scrapy.Field()
    pass
