# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.pipelines.files import FilesPipeline


class WritePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for url in item["file_urls"]:
            yield Request(url)

    def item_completed(self, results, item, info):
        return item

class DfwrwPipeline(object):
    def process_item(self, item, spider):
        return item
