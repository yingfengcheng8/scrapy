# -*- coding: utf-8 -*-
import json,csv,os
from scrapy import Spider,Request,FormRequest
from pyquery import PyQuery as pq

from ibond.items import IbondItem


class SpiderSpider(Spider):
    name = 'spider'
    allowed_domains = ['ibond.chem.tsinghua.edu.cn']
    start_urls = ['http://ibond.chem.tsinghua.edu.cn/pka/','http://ibond.chem.tsinghua.edu.cn/pka/search/']
    baseUrl = 'http://ibond.chem.tsinghua.edu.cn/'
    cookie = {'csrftoken':'IghY4ooNICjaqAioeosVZtDMUTIFpVww','sessionid':'gxt3id7womaqhbbw4hhuljnxt7e3rgus'}

    def start_requests(self):
        if os.path.exists("data/ibond.csv")==False:
            with open("data/ibond.csv", "a+", newline='', encoding='utf-8') as file:
                fieldnames = ['name', 'Structure', 'Solvent', 'solvent_full_name', 'pKa', 'Method',
                              'method_description', 'Ref','ref_content', 'doi']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)

    def parse(self, response):
        doc = pq(response.text)
        for li in doc('#jstree_div ul li').items():
            if len(li.find('.children'))==0:
                fdata = {'csrfmiddlewaretoken': 'IghY4ooNICjaqAioeosVZtDMUTIFpVww', 'input_page_num': '',
                         'input_keyword_type': 'name',
                         'keyword': '', 'input_filter_type': 'pka', 'input_lower': '', 'input_upper': '',
                         'solvent_select': 'All',
                         'cmp_smiles': '', 'similarity_type': 'similarity', 'cutoff': '',
                         'selected_node': li.text()}
                yield FormRequest(self.start_urls[1], callback=self.getItem, formdata=fdata, method='POST',
                                  cookies=self.cookie, meta={'fdata': fdata})

    def getItem(self, response):
        fdata = response.meta['fdata']
        if 'page_num' in fdata.keys():
            count = int(fdata['page_num'])
        else:
            count = 1
        data = json.loads(response.text)
        if len(data['dis_point_list']) > 0:
            for row in data['dis_point_list']:
                name = row['mol_name']
                Structure = self.baseUrl + 'static/media/' + row['img']
                for each in row['dissociation_set']:
                    item = IbondItem()
                    item['name'] = name
                    item['Structure'] = Structure
                    item['Solvent'] = each['solvent__name']
                    item['solvent_full_name'] = each['solvent__full_name']
                    item['pKa'] = each['pKa']
                    item['Method'] = each['method__name']
                    item['method_description'] = each['method__description']
                    item['Ref'] = each['ref__ref_no']
                    item['ref_content'] = each['ref__ref_content']
                    item['doi'] = each['ref__doi']
                    yield item

        if data['paginator']['has_next']:
            count += 1
            fdata['page_num'] = str(count)
            yield FormRequest(self.start_urls[1], callback=self.getItem, formdata=fdata, method='POST',
                              cookies=self.cookie, meta={'fdata': fdata})


