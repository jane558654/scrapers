import scrapy

from tpdb.BaseSceneScraper import BaseSceneScraper
import re
import dateparser
import json
import html
import string
from urllib.parse import urlparse
import time

from datetime import datetime
from tpdb.items import SceneItem

class networkAdultCentroSpider(BaseSceneScraper):
    name = 'AdultCentro'

    sites = {
        'https://aussiefellatioqueens.com',
        'https://www.mylifeinmiami.com',
        'https://cospimps.com',
        'https://daddyscowgirl.com',
        'https://jerkoffwithme.com',
        'https://realagent.xxx',
        'https://facialcasting.com',
        'https://fallinlovia.com',
        'https://bigjohnnyxxx.com',
        'https://dillionation.com',
    }

    selector_map = {
        'title': '',
        'description': '',
        'date': '',
        'image': '',
        'performers': '',
        'tags': '',
        'trailer': '',
        'external_id': r'scene/(\d+)/',
        'pagination': '/home_page=%s'
    }

    def start_requests(self):
        # ~ link = ''
        # ~ if self.site:
            # ~ if self.site in self.sites:
                # ~ link = self.sites[self.site]
        
        # ~ if not link:
            # ~ print(f'Scraper requires a site with -a site=xxxxx flag.')
            # ~ print(f'Current available options are {self.sites}')
            # ~ self.crawler.engine.close_spider(self, reason='No Site Selected')
        # ~ else:
        for link in self.sites:
            yield scrapy.Request(link + '/videos/', callback=self.start_requests_2, meta={'link':link})

    def start_requests_2(self, response):
        
        appscript = response.xpath('//script[contains(text(),"fox.createApplication")]/text()').get()
        meta = response.meta
        if meta['link']:
            if appscript:
                ah = re.search(r'"ah":"(.*?)"', appscript).group(1)
                aet = re.search(r'"aet":([0-9]+?),', appscript).group(1)
                if ah and aet:
                    print(f'ah: {ah}')
                    print(f'aet: {aet}')
                    token = ah[::-1] + "/" + str(aet)
                    print(f'Token: {token}')

            if not token:
                quit()
            else:
                meta['token'] = token

            
            url = self.get_next_page_url(meta['link'], self.page, meta['token'])
            meta['page'] = self.page
            yield scrapy.Request(url, callback=self.parse, meta=meta)

    def parse(self, response, **kwargs):
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
                yield scrapy.Request(url=self.get_next_page_url(response.url, meta['page'], meta['token']),
                                     callback=self.parse,
                                     meta=meta)

    def get_next_page_url(self, base, page, token):
        if "sapi" in base:
            uri = urlparse(base)
            base = uri.scheme + "://" + uri.netloc
        page = str((int(page) - 1) * 10)
        if "miami" in base:
            page_url = base + '/sapi/' + token + '/event.last?_method=event.last&offset={}&limit=10&metaFields[totalCount]=1&transitParameters[v1]=ykYa8ALmUD&transitParameters[v2]=ykYa8ALmUD&transitParameters[showOnHome]=true'
        if "cospimps" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&class=Adultcentro%5CAmc%5CObject%5CContent&limit=10&offset={}&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "jerkoff" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&limit=10&offset={}&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "aussiefellatio" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&limit=10&offset={}&transitParameters[v1]=ykYa8ALmUD&transitParameters[v2]=ykYa8ALmUD&transitParameters[preset]=videos'
        if "daddyscowgirl" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&class=Adultcentro%5CAmc%5CObject%5CContent&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "realagent" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[exceptTags]=extra&transitParameters[preset]=videos'
        if "facialcasting" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "fallinlovia" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "bigjohnnyxxx" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
        if "dillionation" in base:
            page_url = base + '/sapi/' + token + '/content.load?_method=content.load&tz=-4&fields[0]=generatedContentLink&fields[1]=cName&fields[2]=title&fields[3]=_resources.primary.url&fields[4]=sites.publishDate&fields[5]=type&fields[6]=_resources.base.url&fields[7]=_resources.base&fields[8]=length&limit=10&offset={}&metaFields[resources][thumb]=baseline.sprite.w225i&metaFields[totalCount]=1&transitParameters[v1]=OhUOlmasXD&transitParameters[v2]=OhUOlmasXD&transitParameters[preset]=videos'
            
        return self.format_url(base, page_url.format(page))

    def get_scenes(self, response):
        meta = response.meta
        global json
        jsondata = json.loads(response.text)
        jsondata = jsondata['response']['collection']

        for scene in jsondata:
            if "miami" in response.url:
                scene_id = scene['_typedParams']['id']
            else:
                scene_id = scene['id']
            scene_url = self.format_url(response.url, '/sapi/' + meta['token'] + '/content.load?_method=content.load&tz=-4&filter[id][fields][0]=id&filter[id][values][0]=%s&limit=1&transitParameters[v1]=ykYa8ALmUD&transitParameters[preset]=scene' % scene_id)
            yield scrapy.Request(scene_url, callback=self.parse_scene, headers=self.headers, cookies=self.cookies, meta=meta)

    def parse_scene(self, response):
        meta=response.meta
        item = SceneItem()
        global json

        jsondata = response.text
        jsondata = jsondata.replace('\r\n', '')
        try:
            data = json.loads(jsondata.strip())
        except:
            print(f'JSON Data: {jsondata}')

        data = data['response']['collection'][0]

        item['id'] = data['id']
        item['title'] = string.capwords(html.unescape(data['title']))
        item['description'] = html.unescape(data['description'].strip())
        item['date'] = dateparser.parse(data['sites']['collection'][str(item['id'])]['publishDate'].strip()).isoformat()

        if "fallinlovia" in response.url:
            item['performers'] = ['Eva Lovia']
        else:
            item['performers'] = []
            
        item['tags'] = []
        
        if "jerkoff" in response.url or "dillionation" in response.url:
            performers = data['tags']['collection']
            for performer in performers:
                performername = performers[performer]['alias'].strip().title()
                if performername:
                    item['performers'].append(performername)
        elif "daddyscowgirl" not in response.url and "fallinlovia" not in response.url:
            tags = data['tags']['collection']
            for tag in tags:
                tagname = tags[tag]['alias'].strip().title()
                if tagname and "Model - " not in tagname:
                    item['tags'].append(tagname)

        item['url'] = self.format_url(response.url, 'scene/' + str(item['id']))
        item['image'] = data['_resources']['primary'][0]['url']

        if "cospimps" in response.url:
            item['trailer'] = "https://cospimps.com/api/download/{}/hd1080/stream?video=1".format(item['id'])
        if "facialcasting" in response.url:
            item['trailer'] = "https://facialcasting.com/api/download/{}/hd1080/stream".format(item['id'])
        elif "jerkoff" in response.url:
            item['trailer'] = ''
        else:
            item['trailer'] = data['_resources']['hoverPreview']
                        
        if "aussiefellatio" in response.url:
            item['site'] = 'Aussie Fellatio Queens'
            item['parent'] = 'Aussie Fellatio Queens'
            item['network'] = 'Aussie Fellatio Queens'
            modelurl = "https://aussiefellatioqueens.com/sapi/{}/model.getModelContent?_method=model.getModelContent&tz=-4&transitParameters[contentId]={}".format(meta['token'], item['id'])
            meta['item'] = item
            yield scrapy.Request(modelurl, callback=self.get_performers_json, meta=meta)
            
        if "jerkoff" in response.url:
            item['site'] = 'Jerk Off With Me'
            item['parent'] = 'Jerk Off With Me'
            item['network'] = 'Jerk Off With Me'
            yield item
            
        if "fallinlovia" in response.url:
            item['site'] = 'Fall in Lovia'
            item['parent'] = 'Fall in Lovia'
            item['network'] = 'Fall in Lovia'
            yield item
            
        if "dillionation" in response.url:
            item['site'] = 'Dillion Harper'
            item['parent'] = 'Dillion Harper'
            item['network'] = 'Dillion Harper'
            yield item
            
        if "miami" in response.url:
            item['site'] = 'My Life In Miami'
            item['parent'] = 'My Life In Miami'
            item['network'] = 'My Life In Miami'
            item['performers'] = []
            yield item
            
        if "daddyscowgirl" in response.url:
            item['site'] = 'Daddys Cowgirl'
            item['parent'] = 'Daddys Cowgirl'
            item['network'] = 'Daddys Cowgirl'
            item['performers'] = []
            yield item
            
        if "realagent" in response.url:
            item['site'] = 'Real Agent'
            item['parent'] = 'Real Agent'
            item['network'] = 'Real Agent'
            item['performers'] = []
            yield item
            
        if "bigjohnnyxxx" in response.url:
            item['site'] = 'Big Johnny XXX'
            item['parent'] = 'Big Johnny XXX'
            item['network'] = 'Big Johnny XXX'
            item['performers'] = []
            yield item
            
        if "cospimps" in response.url:
            item['site'] = 'Cospimps'
            item['parent'] = 'Cospimps'
            item['network'] = 'Cospimps'
            modelurl = "https://cospimps.com/sapi/{}/model.getModelContent?_method=model.getModelContent&tz=-4&transitParameters[contentId]={}".format(meta['token'], item['id'])
            meta['item'] = item
            yield scrapy.Request(modelurl, callback=self.get_performers_json, meta=meta)
            
        if "facialcasting" in response.url:
            item['site'] = 'Facial Casting'
            item['parent'] = 'Facial Casting'
            item['network'] = 'Facial Casting'
            modelurl = "https://facialcasting.com/sapi/{}/model.getModelContent?_method=model.getModelContent&tz=-4&transitParameters[contentId]={}".format(meta['token'], item['id'])
            meta['item'] = item
            yield scrapy.Request(modelurl, callback=self.get_performers_json, meta=meta)


    def get_performers_json(self, response):
        meta = response.meta
        item = meta['item']

        jsontext = response.text
        performers = re.findall('stageName\":\"(.*?)\"', jsontext)
        if performers:
            item['performers'] = performers
        else:
            item['performers'] = []
        
        yield item
