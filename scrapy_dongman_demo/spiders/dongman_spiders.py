# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy_dongman_demo.items import ScrapyDongmanDemoItem

'''
抓取 图片爬虫

'''

# 全局页数
page_num = 0


class DongmanSpidersSpider(scrapy.Spider):
    name = 'dongman_spiders'
    allowed_domains = ['www.mmonly.cc']
    start_urls = ['http://www.mmonly.cc/ktmh']

    def parse(self, response):
        pic_index_list = response.xpath(
            "//div[@class='Clbc_Game_l_a']//div[@id='infinite_scroll']/div[@class='item masonry_brick masonry-brick']/div[@class='item_t']/div/div[@class='ABox']/a")
        for i in pic_index_list:
            # 遍历节点
            data = ScrapyDongmanDemoItem()
            data['title'] = i.xpath("./img/@alt").extract_first()
            data['url'] = i.xpath("./@href").extract_first()
            data['pic_url'] = i.xpath("./@href").extract_first()
            yield scrapy.Request(
                data['url'], callback=self.parse_detail, meta={"item": data})
        # # 下一页
        # next_url = response.xpath("//div[@id='pageNum']/a[last()-1]/@href").extract()
        # try:
        #     if next_url:
        #         next_link = next_url[0]
        #         # 提交管道进行 下一页处理
        #         yield scrapy.Request("".join(self.start_urls) + "/" + next_link, callback=self.parse)
        # except:
        #     pass

    '''
    获取详细页数据 
    '''

    def parse_detail(self, response):
        item = response.meta["item"]
        xpath_html = response.xpath("//div[@class='photo']/div[@class='wrapper clearfix imgtitle']")
        # 名称前缀
        detail_title_prefix = xpath_html.xpath("./h1/text()").extract()
        # 名称后缀
        detail_title_suffix = xpath_html.xpath("string(./h1/span)").extract()
        # 明细页名称
        item["detail_title"] = "".join(detail_title_prefix + detail_title_suffix)
        # 详细页图片下载地址
        item["down_path"] = xpath_html.xpath("./ul/li[@class='pic-down h-pic-down']/a/@href").extract()
        yield item
        next_url = response.xpath("//div[@class='pages']/ul/li[@id='nl']/a/@href").extract()
        try:
            if next_url and not '##' == next_url[0]:
                next_link = next_url[0]
                # 提交管道进行 下一页处理
                pic_url = item['pic_url']
                next_page_flag = pic_url[pic_url.rfind('/', 1) + 1:len(pic_url) + 1]

                data = ScrapyDongmanDemoItem()
                data['title'] = item['title']
                data['url'] = item['url']
                data['pic_url'] = str(item['pic_url']).replace(next_page_flag, next_link)
                yield scrapy.Request(data['pic_url'], callback=self.parse_detail, meta={"item": data})
        except:
            pass