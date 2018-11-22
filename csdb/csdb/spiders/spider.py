# -*- coding: utf-8 -*-
import csv
from scrapy import Spider, Request, FormRequest
from pyquery import PyQuery as pq
from csdb.items import CsdbItem

class SpiderSpider(Spider):
    name = 'spider'
    allowed_domains = ['www.hydrsm.csdb.cn']
    start_urls = ['http://www.hydrsm.csdb.cn/']
    baseUrl = 'http://www.hydrsm.csdb.cn/list.php'

    def start_requests(self):
        with open("data/adsorption.csv", "a+", newline='', encoding='utf-8') as csvfile:
            fieldnames = ['formula', 'name', 'category', 'information', 'Reference', 'Hydrogen_storage', 'optimum_Hydrogen_storage',  'method', 'image']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        for i in range(1,79):
            url = self.baseUrl+'?page='+str(i)
            yield Request(url,callback=self.parseItem)

    def parseItem(self,response):
        doc = pq(response.text)
        tab = doc('.dongtai_lb2 table table table')
        for row in tab.find('.text').items():
            url = self.start_urls[0]+row.attr('href')
            yield Request(url,callback=self.getItem)

    def getItem(self,response):
        item = CsdbItem()
        doc = pq(response.text)
        tab = doc('.dongtai_lb2 table table')
        item['formula'] = tab.find('tr').eq(0).find('td').eq(1).text()
        item['name'] = tab.find('tr').eq(0).find('td').eq(3).text()
        item['category'] = tab.find('tr').eq(1).find('td').eq(1).text()
        item['information'] = tab.find('tr').eq(2).find('td').eq(1).text()
        item['Reference'] = tab.find('tr').eq(3).find('td').eq(1).text()
        item['Hydrogen_storage'] = tab.find('tr').eq(4).find('td').eq(1).text()
        item['optimum_Hydrogen_storage'] = tab.find('tr').eq(5).find('td').eq(1).text()
        item['method'] = tab.find('tr').eq(5).find('td').eq(3).text()
        item['image'] = []
        if tab.find('tr').eq(6):
            for img in tab.find('tr').eq(6).find('img').items():
                src = self.start_urls[0]+img.attr('src')
                item['image'].append(src)
        # print('>>>>>>>>>>',item['name'])
        yield item