# -*- coding: utf-8 -*-
import scrapy
import re

class RenminSpider(scrapy.Spider):
    name = 'renmin'
    today = '2017-07/28'
    allowed_domains = ['paper.people.com.cn']
    start_urls = ['http://paper.people.com.cn/rmrb/html/' + today +'/nbs.D110000renmrb_01.htm']
    def parse(self, response):
        today = '2017-07/28'
        for part in response.css('div.right_title-name').extract():
            try:
                id = re.findall(r'nbs\.D\d{6}renmrb_\d{2}',part)[0]
                url = 'http://paper.people.com.cn/rmrb/html/' + today + '/' + id + '.htm'
            except:
                continue
            yield scrapy.Request(url, callback=self.parse_part)

    def parse_part(self, response):
        today = '2017-07/28'
        for news in response.css('div[style=\'display:inline\']').extract():
            try:
                id = re.findall(r'nw\.D\d{6}renmrb_\d{8}_\d-\d{2}',news)[0]
                url = 'http://paper.people.com.cn/rmrb/html/' + today + '/' + id + '.htm'
            except:
                continue
            yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):
        news = {}
        content = ''
        for text in response.css('P').extract():
            if text != response.css('P').extract()[-1] and text != response.css('P').extract()[-2]:
                content = content + text[3:-4]
        title = response.css('h3').extract()[0][4:-5] + '\n' + response.css('h1').extract()[0][4:-5] + '\n' +response.css('h2').extract()[0][4:-5]
        news[title] = content
        yield news
