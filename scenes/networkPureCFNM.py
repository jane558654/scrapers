import scrapy
import re
import dateparser
from urllib.parse import urlparse

from tpdb.items import SceneItem
from tpdb.BaseSceneScraper import BaseSceneScraper


class networkPureCFNMSpider(BaseSceneScraper):
    name = 'PureCFNM'
    network = 'Pure CFNM'
    parent = 'Pure CFNM'

    start_urls = [
        ['https://www.purecfnm.com', '/categories/purecfnm_%s_d.html', 'Pure CFNM'],
        ['https://www.ladyvoyeurs.com', '/categories/lady-voyeurs_%s_d.html', 'Lady Voyeurs'],
        ['https://www.amateurcfnm.com', '/categories/amateur-cfnm_%s_d.html', 'Amateur CFNM'],
        ['https://www.cfnmgames.com', '/categories/cfnm-games_%s_d.html', 'CFNM Games'],
        ['https://www.girlsabuseguys.com', '/categories/girls-use-guys_%s_d.html', 'Girls Abuse Guys'],
        ['https://littledick.club', '/categories/movies_%s_d.html', 'Little Dick Club'],
    ]

    selector_map = {
        'title': '',
        'description': '',
        'date': '',
        'image': '',
        'performers': '',
        'tags': '',
        'external_id': 'view\/(\d+)\/',
        'trailer': '',
        'pagination': '/videos?order=publish_date&sort=desc&page=%s'
    }



    def start_requests(self):
        for link in self.start_urls:
            yield scrapy.Request(url=self.get_next_page_url(link[0], self.page, link[1]),
                                 callback=self.parse,
                                 meta={'page': self.page, 'pagination':link[1], 'site':link[2], 'url':link[0]},
                                 headers=self.headers,
                                 cookies=self.cookies)

    def parse(self, response, **kwargs):
        if response.status == 200:
            scenes = self.get_scenes(response)
            count = 0
            for scene in scenes:
                count += 1
                yield scene

            if count:
                if 'page' in response.meta and response.meta['page'] < self.limit_pages:
                    meta = response.meta
                    meta['page'] = meta['page'] + 1
                    print('NEXT PAGE: ' + str(meta['page']))
                    url = meta['url']
                    yield scrapy.Request(url=self.get_next_page_url(url, meta['page'], meta['pagination']),
                                         callback=self.parse,
                                         meta=meta,
                                         headers=self.headers,
                                         cookies=self.cookies)


    def get_next_page_url(self, base, page, pagination):
        return self.format_url(base, pagination % page)
        
    def get_scenes(self, response):
        meta = response.meta
        
        scenes = response.xpath('//div[@class="update_details"]')
        for scene in scenes:
            item = SceneItem()
            
            title = scene.xpath('./comment()[contains(.,"Title")]/following-sibling::a/text()').get()
            if title:
                item['title'] = title.strip()
            
            date = scene.xpath('.//div[contains(@class,"update_date")]/comment()/following-sibling::text()').get()
            if date:
                item['date'] = dateparser.parse(date.strip()).isoformat()
            else:
                item['date'] = dateparser.parse('today').isoformat()
            
            performers = scene.xpath('.//span[@class="update_models"]/a/text()').getall()
            if performers:
                item['performers'] = list(map(lambda x: x.strip().title(), performers))
            else:
                item['performers'] = []
            
            image = scene.xpath('./a/img/@data-src0_3x').get()
            if not image:
                image = scene.xpath('./a/img/@data-src0_2x').get()
            if not image:
                image = scene.xpath('./a/img/@data-src0_1x').get()
            if not image:
                image = scene.xpath('./a/img/@src').get()
            if image:
                uri = urlparse(response.url)
                base = uri.scheme + "://" + uri.netloc
                item['image'] = base + image.strip()
            else:
                item['image'] = ''
            
            trailer = scene.xpath('./comment()[contains(.,"Title")]/following-sibling::a[contains(@onclick,"/trailer/")]/@onclick').get()
            if trailer:
                trailer = re.search('tload\(\'(.*.mp4)\'', trailer)
                if trailer:
                    trailer = trailer.group(1)
                    uri = urlparse(response.url)
                    base = uri.scheme + "://" + uri.netloc
                    item['trailer'] = base + trailer.strip()
            else:
                item['trailer'] = ''
                
            item['id'] = scene.xpath('./@data-setid').get()
            item['url'] = response.url
            item['description'] = ''
            item['tags'] = []
            item['site'] = meta['site']
            item['parent'] = meta['site']
            item['network'] = "Pure CFNM"
            
            if item['id'] and item['title']:
                yield item
            
                
