# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http.request import Request
import hashlib
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
import numpy as  np
from urllib.parse import urlparse
import re
import logging
import scrapy
import csv
logger = logging.getLogger('pipelinelogger')
from scrapy.exceptions import DropItem
import json


class ScrapyYelpPipeline(object):

    columns =['slug','categories'	,'distance'	,'name'	,'price_level',	'rating',	'review_count',	'url',	'lat',	'lng',
    	'Sp1',	'type' ,	'homeurl',	'resource_id1'	,'resource_id2'	,'lat2',	'lng2']


    # columns =['resource_id', 'lat', 'lng', 'type', 'biz.alias', 'biz.review_count',
    #    'biz.name', 'biz.rating', 'biz.url', 'biz.price', 'biz.categories',
    #    'biz.distance', 'url', 'resourceId', 'hovercardId', 'location.latitude',
    #    'location.longitude']

    aggregate_filename="summary.csv"
    menu_filename = "menu.csv"

    def open_spider(self, spider):
        # write header for summary data
        if not os.path.exists(self.aggregate_filename):
            print(self.aggregate_filename,"----- not exists!!")
            x =  self.columns # np.sort(self.columns)
            np.array(x).tofile(self.aggregate_filename, ',', '%s')
            # write extra return  for first time
            with open(self.aggregate_filename, mode='a') as f:
                f.write("\n")
        # write header for menu data
        if not os.path.exists(self.menu_filename):
            print(self.menu_filename,"----- not exists!!")
            with open(self.menu_filename,'w') as out:
                csv_out=csv.writer(out)
                csv_out.writerow(['slug','title','desc','price'])

    def close_spider(self, spider):
        pass
        #self.file.close()

    def process_item(self, item, spider):
        # append to file
        if 'df' in item:
            df=item["df"]
            df.to_csv(self.aggregate_filename,index=False,header=False,encoding='utf-8',mode='a')

        if 'menuitems' in item:
            menuitems=item["menuitems"]
            slug=item["slug"]

            with open(self.menu_filename,'a') as out:
                csv_out=csv.writer(out)
                for row in menuitems:
                    csv_out.writerow(row)

        return item




class MyImagesPipeline(ImagesPipeline):
    def image_key(self, url):
        image_guid = url.split('/')[-1]
        return 'yelp_images/%s' % (image_guid)
