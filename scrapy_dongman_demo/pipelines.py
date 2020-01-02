# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


'''
管道数据处理
两个管道 一个管道输出item传递给下一个
'''
import os
import re
from scrapy import Request

from scrapy.pipelines.images import ImagesPipeline


class ScrapyDongmanDemoPipeline(object):
    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'], re.S))
        path = 'E:\\动漫图\\{}'.format(title)
        # print("开始下载动漫图:{},详细页:{}]".format(title, item['detail_title']))
        # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
        if not os.path.exists(path):
            os.makedirs(path)
            # 获取下载的文件名称
        item["info_down_path"] = path + "\\" + "".join(
            re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',
                       str(item['detail_title']).format("(", "第").replace("/", "分").replace(")", "页"), re.S)) + ".jpg"
        return item


class ImagesspiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        '''获取图片的url,通过Request方法，保存图片'''
        # 这里meta={'item': item},目的事件item传递到file_path中
        return Request(item['down_path'][0], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        '''图片保存的路径'''
        item = request.meta['item']
        return item["info_down_path"]
