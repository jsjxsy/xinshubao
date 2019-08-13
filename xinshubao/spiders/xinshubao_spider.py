# -*- coding: utf-8 -*-
import os

import scrapy
import logging
import re

from xinshubao.items import XinshubaoItem, StoryContent, StoryChapterContent


class XinshubaoSpiderSpider(scrapy.Spider):
    # referer_url = "http://www.xinshubao.net/xiaoshuodaquan/"
    # default_headers = {
    #     'accept': 'image/webp,image/*,*/*;q=0.8',
    #     'accept-encoding': 'gzip, deflate, sdch, br',
    #     'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
    #     'cookie': 'bid=yQdC/AzTaCw',
    #     'referer': referer_url,
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    # }

    name = 'xinshubao_spider'
    allowed_domains = ['www.xiaoshubao.net']
    start_urls = ['http://www.xinshubao.net/xiaoshuodaquan/']

    def parse(self, response):
        story_link = response.xpath("//div[@class='novellist']/ul/li/a/@href").extract()
        for story_item_link in story_link:
            request_url = "http://www.xinshubao.net" + story_item_link
            # if request_url in "http://www.xinshubao.net/10/10000/":
            #     request_url = "http://www.xinshubao.net/43/43389/"
            logging.info(request_url)
            yield scrapy.Request(url=request_url, callback=self.parse_home_page, dont_filter=True)

    def parse_home_page(self, response):
        story_item = XinshubaoItem()
        name = response.xpath("//div[@id='info']/h1/text()").extract()
        logging.info(name[0])
        story_item['name'] = name[0]

        author = response.xpath("//div[@id='info']/p[1]/text()").extract()
        logging.info(author[0])
        story_item['author'] = author[0]

        story_status = response.xpath("//div[@id='info']/p[2]/text()").extract()
        logging.info(story_status[0])
        story_item['story_status'] = story_status[0]

        lasted_update = response.xpath("//div[@id='info']/p[3]/text()").extract()
        logging.info(lasted_update[0])
        story_item['lasted_update'] = lasted_update[0]

        story_description = response.xpath("//div[@id='intro']/p/text()").extract()
        logging.info(story_description[0])
        story_item['story_description'] = story_description[0]
        yield story_item

        story_content_list = response.xpath("//ul[@class='_chapter']/li")
        for story_content_item in story_content_list:
            story_content = StoryContent()
            story_chapter = story_content_item.xpath("./a/text()").extract()
            logging.info(story_chapter[0])
            story_content['story_chapter'] = story_chapter[0]

            story_chapter_url = story_content_item.xpath("./a/@href").extract()
            temp = story_chapter_url[0].strip();
            story_chapter_url_link = re.sub('[\r\n\t]', '', temp)
            logging.info(story_chapter_url_link)
            story_content['story_chapter_url'] = story_chapter_url_link
            # yield story_content
            #if story_chapter_url_link in "http://www.xinshubao.net/10/10000/696372.html":
            pos = story_chapter_url_link.rfind(".")
            story_link_suffix = story_chapter_url_link[:pos]
            logging.info("story_link_suffix==>" + story_link_suffix)
            yield scrapy.Request(url=story_chapter_url_link,
                                 meta={'story_name': name[0], "url_suffix": story_link_suffix},
                                 callback=self.parse_content_page,
                                 dont_filter=True)

    def parse_content_page(self, response):
        story_chapter_content = ""
        story_chapter_content_item = StoryChapterContent()
        story_chapter_content_item['story_name'] = response.meta['story_name']

        story_content = response.xpath("//div[@id='content']/text()").extract()
        story_chapter_content = story_chapter_content.join(story_content)
        # for story_content_item in story_content:
        #     story_chapter_content += story_content_item

        # logging.info(story_chapter_content)
        story_chapter_content_item['story_chapter_content'] = story_chapter_content

        story_chapter_name = response.xpath("//div[@class='bookname']/h1/text()").extract()
        logging.info(story_chapter_name[0])

        story_chapter_content_item['story_chapter_name'] = story_chapter_name[0]
        yield story_chapter_content_item

        next_chapter_url = response.xpath("//div[@class='bottem1']/p[2]/a[4]/@href").extract()[0]
        logging.info("next_chapter_url==>" + next_chapter_url)
        if not next_chapter_url.startswith("http"):
            story_chapter_url_suffix = response.meta['url_suffix'];
            pos = story_chapter_url_suffix.rfind("/")
            next_chapter_link = story_chapter_url_suffix[:pos] + '/' + next_chapter_url
            logging.info("next_chapter_link==>" + next_chapter_link)

            if next_chapter_link.startswith(story_chapter_url_suffix):
                yield scrapy.Request(url=next_chapter_link,
                                     meta={'story_name': story_chapter_content_item['story_name'],
                                           "url_suffix": story_chapter_url_suffix},
                                     callback=self.parse_content_page,
                                     dont_filter=True)
            else:
                print(
                    "no start story_chapter_url_suffix:" + story_chapter_url_suffix
                    + " next_chapter_link:" + next_chapter_link)
        else:
            print("not start http next_chapter_url:" + next_chapter_url)
        pass
