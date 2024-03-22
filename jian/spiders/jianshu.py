# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jian.items import JianItem


class JianshuSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}'), callback='parse_detail', follow=True),
    )

    # /html/head/title
    # /html/head/meta[@name="description"]
    # /html/head/meta[@name="keywords"]

    def parse_detail(self, response):
        title = response.xpath('//section/h1//text()').get()
        auther = response.xpath('//section/div[position()=1]/div//span[position()=1]//text()').get().strip()
        article = ",".join(response.xpath('//section[position()=1]/article//text()').getall())
        avatar = response.xpath('//section[position()=1]/div[position()=1]/div//img/@src').get()
        article_id = response.url.replace("https://www.jianshu.com/p/", "")
        time_out = response.xpath('/html/body/div//section[1]//time[1]//text()').get()

        try:
            try:
                read_number = response.xpath(
                    '/html/body//section[1]/div[2]/div/div/div[2]/span[3]//text()').get().replace("阅读 ", "")
            except:
                read_number = response.xpath(
                    '/html/body//section[1]/div[2]/div/div/div[2]/span[2]//text()').get().replace("阅读 ", "")
        except:
            read_number = 0

        meta_title = response.xpath('/html/head/title//text()').get()
        meta_description = response.xpath('/html/head/meta[@name="description"]/@content').get()
        meta_keywords = response.xpath('/html/head/meta[@name="keywords"]/@content').get()

        item = JianItem(
            title=title,
            auther=auther,
            article=article,
            time_out=time_out,
            read_number=read_number,
            avatar=avatar,
            article_id=article_id,  # 注意必须是元组
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords
        )
        yield item
