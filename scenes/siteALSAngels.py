import re
import scrapy
import tldextract
import dateparser

from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem

### All the videos are on one long, page, but the logic should handle the
### normal "limit_pages" values

class siteALSAngelsSpider(BaseSceneScraper):
    name = 'ALSAngels'
    network = "ALS Angels"
    parent = "ALS Angels"

    start_urls = [
        'http://www.alsangels.com/',
    ]

    selector_map = {
        'title': '',
        'description': '',
        'date': '',
        'date_formats': ['%d %b %Y'],
        'image': '',
        'performers': '',
        'tags': '',
        'external_id': '',
        'trailer': '',
        'pagination': ''
    }
    

    def start_requests(self):
        url = "http://www.alsangels.com/dailyvideos.html"
        yield scrapy.Request(url, callback=self.get_scenes,
                             headers=self.headers,
                             cookies=self.cookies)    

    def get_scenes(self, response):
        
        if self.limit_pages:
            if isinstance(self.limit_pages, int):
                scenelimit = self.limit_pages * 20
            elif self.limit_pages.lower() == "all":
                scenelimit = 9999
        else:
            scenelimit = 20
            
        scenecounter = 1
        
        scenes = response.xpath('//tr')
        for scene in scenes:
            item = SceneItem()
                
            tags = scene.xpath('./td[@class="videotext"]//span[@class="videotype"]/text()').get()
            if tags:
                tags = tags.replace("Video Type: ", "").strip()
                item['tags'] = [tags]
            else:
                item['tags'] = []       
                
                
            performerlist = scene.xpath('./td[@class="videotext"]//h2//text()').get()
            if performerlist:
                performerlist = performerlist.title()
                performerlist = performerlist.replace("Model: ", "").strip()
                performerlist = performerlist.replace("Models: ", "").strip()
                titletext = performerlist
                
                performerlist = re.sub('[^a-zA-Z,:& ]', '', performerlist)
                performerlist = performerlist.replace("Shoot ", "").strip()
                performerlist = performerlist.replace("Body Painting", "").strip()
                performerlist = performerlist.replace("Nude In Public", "").strip()
                performerlist = performerlist.replace("With ", "& ").strip()
                performerlist = performerlist.replace(", ", " & ").strip()
                performerlist = performerlist.replace(" And ", " & ").strip()
                performerlist = performerlist.replace("  ", " ").strip()
                
                item['performers'] = performerlist.split("&")
                item['performers'] = list(map(lambda x: x.strip(), item['performers']))
                
                item['title'] = titletext + " " + item['tags'][0]
            else:
                item['title'] = ""
                item['performers'] = []            
                                         
            extern_id = scene.xpath('./td[@class="videotext"]/a/@name').get()
            if extern_id:
                item['id'] = extern_id.strip()
            else:
                extern_id = scene.xpath('./td[@class="videothumbnail"]//img/@src').get()
                if extern_id:
                    extern_id = re.search('.*\/(.*).jpg', extern_id).group(1)
                    if extern_id:
                        item['id'] = extern_id.strip()
            
            if not extern_id:
                item['id'] = "123123"
                
            
            image = scene.xpath('./td[@class="videothumbnail"]/a/@href').get()
            if image:
                image = re.search('\(\'(.*.jpg)\'', image).group(1)
            else:
                image = scene.xpath('./td[@class="videothumbnail"]//img/@src').get()
            if image:
                item['image'] = "http://www.alsangels.com/" + image.strip()
            else:
                item['image'] = ''

                
            date = scene.xpath('./td[@class="videotext"]/span[@class="videodate"]/text()').get()
            if date:
                date = date.replace("Date: ", "").strip()
                item['date'] = dateparser.parse(date).isoformat()
            else:
                item['date'] = dateparser.parse('today').isoformat()

            description = scene.xpath('./td[@class="videotext"]//span[@class="videodescription"]/text()').get()
            if description:
                item['description'] = description.strip()
            else:
                item['description'] = ''


            
            url = scene.xpath('./td[@class="videotext"]/a/@href').get()
            if url:
                item['url'] = "http://www.alsangels.com/" + url.strip()
            else:
                item['url'] = response.url
                


            item['site'] = "ALS Angels"
            item['parent'] = "ALS Angels"
            item['network'] = "ALS Angels"
            item['trailer'] = ''
            
            if item['id'] and item['title'] and item['date']:
                yield item

            scenecounter += 1
            if scenecounter > scenelimit:
                break
