import re

import scrapy
from tpdb.BaseSceneScraper import BaseSceneScraper


class AdultEmpireCashScraper(BaseSceneScraper):
    name = 'AdultEmpireCash'
    network = 'AdultEmpireCash'

    start_urls = [
        'https://www.mypervyfamily.com/',
        'https://jayspov.net',
        'https://www.filthykings.com/',
        'https://thirdworldxxx.com',
        'https://latinoguysporn.com',
        'https://cospimps.com/',
        'https://pmggirls.com/',
        'https://www.lethalhardcore.com',
        'https://spankmonster.com',
    ]

    selector_map = {
        'title': '//h1[@class="description"]/text()',
        'description': '//div[@class="synopsis"]/p/text()',
        'date': '//div[@class="release-date"]/text()',
        'image': '//meta[@property="og:image"]/@content',
        'performers': '//div[@class="video-performer"]//img/@title',
        'tags': '//div[@class="tags"]//a/text()',
        'external_id': '(\\d+)/(.+)\\.html',
        'trailer': '',
        'pagination': '/watch-newest-clips-and-scenes.html?page=%s&hybridview=member'
    }

    def get_scenes(self, response):
        if "spankmonster" in response.url:
            scenes = response.xpath('//div[@class="animated-screenshot-container"]/a/@href').getall()
            for scene in scenes:
                meta = {}
                meta['site'] = "Spank Monster"
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)
        else:
            scenes = response.css('.grid-item')
            for scene in scenes:
                link = scene.css('a.grid-item-title::attr(href)').get()
                meta = {}
                if scene.css('p>span::text').get():
                    text = scene.css('p>span::text').get().strip().split('|')
                    if len(text) == 2:
                        meta['site'] = text[0].strip()
                yield scrapy.Request(url=self.format_link(response, link), callback=self.parse_scene, meta=meta)

    def get_site(self, response):
        if 'jayspov' in response.url:
            return 'Jays POV'

        return response.xpath('//div[@class="studio"]//span[2]/text()').get().strip()


    def get_next_page_url(self, base, page):
        pagination = self.get_selector_map('pagination')
        
        if "mypervyfamily" in base:
            pagination = "/my-pervy-family.html?page=%s&view=grid"
        if "jayspov" in base:
            pagination = "/jays-pov-updates.html?page=%s&hybridview=member"
        if "lantinoguys" in base:
            pagination = "/watch-newest-latino-guys-porn-clips-and-scenes.html?page=%s&hybridview=member"
        if "cospimps" in base:
            pagination = "/videos/videos_page=%s"
        if "pmggirls" in base:
            pagination = "/videos/videos_page=%s"
        if "lethalhardcore" in base:
            pagination = "/watch-lethal-hardcore-streaming-video-scenes.html?page=%s&hybridview=member"
        if "spankmonster" in base:
            pagination = "/watch-newest-spank-monster-clips-and-scenes.html?page=%s&hybridview=member"
        return self.format_url(base, pagination % page)
