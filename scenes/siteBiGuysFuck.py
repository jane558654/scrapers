import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper
import re
import dateparser
import json
import html

from datetime import datetime
from tpdb.items import SceneItem

class BiGuysFuckSpider(BaseSceneScraper):
    name = 'BiGuysFuck'
    network = "Bi Guys Fuck"
    parent = "Bi Guys Fuck"

    start_urls = [
        'https://www.biguysfuck.com',
    ]

    selector_map = {
        'title': '',
        'description': '',
        'date': '',
        'image': '',
        'performers': '',
        'tags': '',
        'trailer': '',
        'external_id': '.*\/(.*?)$',
        'pagination': '/videos?page=%s'
    }

    def get_scenes(self, response):

        scenes = response.xpath(
            '//div[contains(@class,"videoPreview")]/a/@href').getall()
        for scene in scenes:
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)


    def parse_scene(self, response):
        item = SceneItem()
        global json
        
        jsondata = response.xpath('//script[@type="application/ld+json"]/text()').get()
        jsondata = jsondata.replace("\r\n","")
        try:
            data = json.loads(jsondata.strip())
        except:
            print (f'JSON Data: {jsondata}')
        data = data[0]
        
        item['title'] = html.unescape(data['name'])
        item['description'] = html.unescape(data['description'].strip())
        
        item['date'] = dateparser.parse(data['uploadDate'].strip()).isoformat()

        tags = data['keywords'].split(",")
        item['tags'] = list(map(lambda x: x.strip().title(), tags))
        
        item['performers'] = list(
            map(lambda x: x['name'].strip(), data['actor']))

        item['url'] = response.url
        item['image'] = data['thumbnailUrl'].replace(" ", "%20")
        item['trailer'] = ''
        item['site'] = 'Bi Guys Fuck'
        item['parent'] = 'Bi Guys Fuck'
        item['network'] = 'Bi Guys Fuck'
        item['id'] = re.search('.*\/(.*?)$',response.url).group(1)
        
        if self.debug:
            print(item)
        else:
            yield item
