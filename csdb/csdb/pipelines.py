# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request,FormRequest
logger=logging.getLogger('Mylog')

class CsdbPipeline(object):
    def process_item(self, item, spider):
        if item['formula']:
            with open("data/adsorption.csv", "a+", newline='', encoding='utf-8') as csvfile:  
                fieldnames = ['formula', 'name', 'category', 'information', 'Reference', 'Hydrogen_storage', 'optimum_Hydrogen_storage',  'method', 'image']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(item)
                logger.info(">>>>>SUCCESS WRITER %s",item['formula'])
            return item
        else:
            return DropItem('Missing Text')

# class FilePipeline(FilesPipeline):
#     def get_media_requests(self, item, info):
#         print('>>>>>>>>>>',item['image'])
#         for url in item['image']:
#             print('>>>>>>>>>>',url)
#             yield Request(url)

#     def file_path(self, request, response=None, info=None):#重命名模块
#         # item = request.meta['item']
#         FilePath = request.url.split('/')[-2]+'/'+request.url.split('/')[-1]
#         return FilePath

#     def item_completed(self, results, item, info):
#         file_paths = [x['path'] for ok, x in results if ok]
#         if not file_paths:
#             raise DropItem("Item contains no files")
#         logger.info('>>>>>>>DOWNLOAD SUCCESS %s', item['formula'])
#         return item