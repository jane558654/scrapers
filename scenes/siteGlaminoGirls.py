from datetime import datetime
import string
import html
import scrapy
import re
import dateparser
import tldextract

from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem

class siteGlaminoGirlsSpider(BaseSceneScraper):
    name = 'GlaminoGirls'
    network = 'Czech Casting'

    start_urls = [
        'https://glaminogirls.com',
        'https://lifepornstories.com',
    ]

    selector_map = {
        'title': "//h2[@class='nice-title']/text()",
        'description': "//div[@class='desc-text']//p/text()",
        'image': "//meta[@property='og:image']/@content",
        're_image': '(.*)\?',
        'tags': '//ul[@class="tags"]/li/a/text()',
        'external_id': '/tour\\/preview\\/(.+)/',
        'trailer': '',
        'pagination': '/tour/page-%s/'
    }

    def get_scenes(self, response):
        scenes = response.xpath('//div[contains(@class,"episode__preview")]')
        for scene in scenes:
            item = SceneItem()

            item['title'] = ''
            title = scene.xpath('.//h2/text()').get()
            if title:
                item['title'] = html.unescape(string.capwords(title.strip()))
                
            item['image'] = ''
            image = scene.xpath('.//div[@class="thumbnail_wrapper"]/img/@src').get()
            if image:
                image = re.search('(.*)\?', image)
                if image:
                    item['image'] = image.group(1).strip()
            
            item['performers'] = []
            performers = scene.xpath('.//span[@class="episode__artist__name"]/text()').get()
            if performers:
                item['performers'] = [html.unescape(string.capwords(performers.strip()))]
                
            item['url'] = ''
            item['id'] = ''
            url = scene.xpath('.//div[contains(@class,"description")]/a/@href').get()
            if url:
                item['url'] = "https://" + tldextract.extract(response.url).domain + ".com" + url.strip()
                item['id'] = re.search('.*\/(.*?)\/', url).group(1)
                
            item['date'] = dateparser.parse('today').isoformat()
            item['description'] = ''
            item['tags'] = ''
            item['trailer'] = ''
            
            
            item['network'] = 'Czech Casting'
            if "glaminogirls" in response.url:
                item['parent'] = "Glamino Girls"
                item['site'] = "Glamino Girls"
            if "lifepornstories" in response.url:
                item['parent'] = "Life Porn Stories"
                item['site'] = "Life Porn Stories"

            if item['id'] and item['title']:
                yield item
