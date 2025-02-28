import string
import html
import re
from datetime import date
import dateparser

from tpdb.BaseSceneScraper import BaseSceneScraper
from tpdb.items import SceneItem


class SiteYanksSpider(BaseSceneScraper):
    name = 'Yanks'
    network = 'Yanks'
    max_pages = 20

    start_urls = [
        'https://www.yanks.com'
    ]

    selector_map = {
        'title': '//h1[contains(@class, "title")]/text()',
        'description': '//p[contains(@class, "description")]/text()',
        'performers': '//span[contains(@class,"models")]/a/text()',
        'date': '//div[contains(@class, "date")]/text()',
        'image': '//meta[@property="og:image"]/@content',
        'tags': '//div[contains(@class, "video-tags")]/a/text()',
        'trailer': '',
        'external_id': r'trailers/(.*)\.html',
        'pagination': '/categories/Movies/%s/latest/'
    }

    def get_scenes(self, response):
        meta = response.meta
        scenes = response.xpath('//div[contains(@class,"videoblock")]')
        if response.meta['page'] < self.max_pages:
            for scene in scenes:
                item = SceneItem()
                title = scene.xpath('.//h3/a/text()').get()
                if title:
                    item['title'] = html.unescape(string.capwords(title))
                else:
                    item['title'] = ''

                item['description'] = ''

                performers = scene.xpath('.//p[contains(text(),"Featuring")]/a/text()')
                if performers:
                    performers = performers.getall()
                    for performer in performers:
                        if "&" in performer:
                            performers.remove(performer)
                    item['performers'] = list(map(lambda x: x.strip(), performers))
                else:
                    item['performers'] = []

                date_xpath = scene.xpath('.//p[contains(text(),"Featuring")]//text()')
                item['date'] = dateparser.parse('today').isoformat()
                if date_xpath:
                    today = date.today()
                    lastyear = today.year - 1
                    todaypart = today.strftime('%m/%d')
                    date_xpath = date_xpath.getall()
                    date_xpath = "".join(date_xpath)
                    datepart = re.search(r'(\d{2}/\d{2})', date_xpath)
                    if datepart:
                        datepart = datepart.group(1)
                        if datepart > todaypart or (datepart < todaypart and meta['page'] > 9):
                            datepart = datepart + "/" + str(lastyear)
                        else:
                            datepart = datepart + "/" + today.strftime('%y')
                        date_result = dateparser.parse(datepart, date_formats=['%m/%d/%Y']).isoformat()
                        item['date'] = date_result

                image = scene.xpath('.//div[@class="videoimg"]/a/img/@src')
                if image:
                    image = image.get()
                    item['image'] = image.strip()
                else:
                    item['image'] = []

                item['tags'] = []
                item['trailer'] = ''
                item['site'] = "Yanks"
                item['parent'] = "Yanks"
                item['network'] = "Yanks"

                extern_id = re.search(r'.*/(\d+).jpg', item['image'])
                if extern_id:
                    item['id'] = extern_id.group(1).strip()

                item['url'] = response.url

                yield item
