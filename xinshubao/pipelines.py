# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import io
import os
import logging

from xinshubao.items import StoryChapterContent, XinshubaoItem


class XinshubaoPipeline(object):

    def process_item(self, item, spider):
        target_path = '/Users/admin/PycharmProjects/xinshubao/'
        # 获取当前工作目录
        if isinstance(item, StoryChapterContent):
            target_path = target_path + item['story_name']
            if not os.path.exists(target_path):
                self.mkdir(target_path)

            filename_path = target_path + os.path.sep + item['story_chapter_name'].replace('/', '_') + '.txt'
            logging.info("filename_path===>" + filename_path)
            with io.open(filename_path, 'w', encoding='utf-8') as f:
                f.write(item['story_chapter_content'] + '\n')
        else:
            logging.info("item is not StoryChapterContent")

        return item

    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            print
            path + ' 创建成功'
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print
            path + ' 目录已存在'
        pass
