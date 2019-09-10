# -*- coding: utf-8 -*-
import scrapy
from tecnoblog.items import TecnoblogItem

class TecnoblogSpider(scrapy.Spider):
    name = 'Tecnoblog'
    allowed_domains = ['tecnoblog.net']
    start_urls = ['https://tecnoblog.net/page/2']

    def parse(self, response):
        try:
            for article in response.css('article'):
                link = article.css('div.texts h2 a::attr(href)').extract_first() 
                yield response.follow(link,self.parse_article)
        
            next_page = response.css('a#mais::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
        except Exception:
            print("Ocorreu erro no Parse")

    def parse_article(self, response):        
        link = response.url
        title = response.css('title ::text').extract_first()
        author = response.css('span.author ::text').extract_first()
        # text = "".join(response.css('div.entry ::text').extract()).strip()
        text = ""

        item = TecnoblogItem(link=link,author=author,title=title,text=text)

        yield item
