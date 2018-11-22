# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
logger = logging.getLogger('MYLOG')

class IbondPipeline(object):
    def process_item(self, item, spider):
        if item['name']:
            with open("data/ibond.csv", "a+", newline='', encoding='utf-8') as file:
                fieldnames = ['name','Structure','Solvent','solvent_full_name','pKa','Method','method_description','Ref','ref_content','doi']
                writer = csv.DictWriter(file,fieldnames=fieldnames)
                writer.writerow(item)
            print('SUCCESS WRITE_TO_CSV：',item['Solvent'])
            return item
        else:
            return DropItem('Missing Text')

class ImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(item['Structure'])

    def file_path(self, request, response=None, info=None):
        file_name = request.url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        else:
            logger.info('++++++++SUCCESS Download Image %s',item['name'])
        return item