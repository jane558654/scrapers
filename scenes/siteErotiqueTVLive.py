import scrapy
import re
import dateparser

from tpdb.BaseSceneScraper import BaseSceneScraper


class siteErotiqueTVLiveSpider(BaseSceneScraper):
    name = 'ErotiqueTVLive'
    network = 'ErotiqueTVLive'
    parent = 'ErotiqueTVLive'

    start_urls = [
        'https://erotiquetvlive.com',
    ]

    selector_map = {
        'title': '//div[@class="video-player"]/div/h2/text()',
        'description': '//h3[contains(text(), "Description")]/following-sibling::text()',
        'date': '',
        'image': '//div[@class="player-thumb"]//img/@src0_1x',
        'performers': '//div[contains(@class,"models-list-thumbs")]/ul/li/a/span/text()',
        'tags': '//div[@class="update-info-block"]/ul/li/a/text()',
        'external_id': '.*\/(.*?).html',
        'trailer': '',
        'pagination': '/tour/categories/movies_%s_d.html'
    }

    def get_scenes(self, response):
        scenes = response.xpath('//div[@class="content-div"]/h4/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)

    def get_site(self, response):
        return "ErotiqueTVLive"

    def get_parent(self, response):
        return "ErotiqueTVLive"
        
    def get_date(self, response):
        return dateparser.parse('today').isoformat()
        
