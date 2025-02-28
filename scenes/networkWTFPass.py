import scrapy
import re
import tldextract
from dateutil.relativedelta import relativedelta
import dateparser
import datetime
import string
import html

from tpdb.BaseSceneScraper import BaseSceneScraper

# ~ Network contains the following sites:
     # ~ College Fuck Parties 
     # ~ Dolls Porn 
     # ~ Hard Fuck Girls 
     # ~ HD Massage Porn 
     # ~ Meet Suck And Fuck 
     # ~ Panda Fuck 
     # ~ Pickup Fuck 
     # ~ Porn Weekends 
     # ~ Private Sex Tapes 
     # ~ Public Sex Adventures 
     # ~ The Art Porn 


class networkWTFPassSpider(BaseSceneScraper):
    name = 'WTFPass'
    network = 'WTF Pass'


    start_urls = [
        'https://wtfpass.com',
    ]

    selector_map = {
        'title': '//meta[@property="og:title"]/@content',
        'description': '//meta[@name="description"]/@content',
        'date': '',  #Site does not have valid dates, so it is calculated from xx Days/Months/Years ago
        'image': '//meta[@property="og:image"]/@content',
        'performers': '//div[@class="data-row data-actress"]/a/text()',
        'tags': '//div[contains(@class,"tab-info")]/div[@class="data-row"]/a/text()',
        'external_id': 'videos\/(\d+)\/',
        'trailer': '',
        'pagination': '/videos/%s/'
    }

    def get_scenes(self, response):
        meta = {}
        scenes = response.xpath('//div[@class="thumb-video cf"]')
        for scene in scenes:
            
            meta['date'] = dateparser.parse('today').isoformat()
            date = scene.xpath('.//span[@class="date-added"]/text()')
            if date:
                date = date.get()
                date = parse_date(date)
                if date:
                    meta['date'] = date
            
            scene = scene.xpath('./div/a[contains(@href,"/videos/")]/@href').get()
            if re.search(self.get_selector_map('external_id'), scene):
                yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene, meta=meta)

    def get_site(self, response):
        site = response.xpath('//div[contains(@class,"tab-info")]/div/span[@class="site"]/a/text()').get()
        if site:
            return site.strip()

        return tldextract.extract(response.url).domain


    def get_parent(self, response):
        return "WTF Pass"
        


    def get_description(self, response):
        description = self.process_xpath(response, self.get_selector_map('description')).get()
        if description:
            if "Reality porn videos from hot college sex" in description:
                return ''
            else:
                return html.unescape(description.strip())

        return ''


def parse_date(datestring):
    today = datetime.datetime.now()
    datestring = datestring.lower()
    intervalcount = re.search('(\d+)', datestring).group(1)
    if not intervalcount:
        intervalcount = 0
    else:
        intervalcount = int(intervalcount)
    if "minutes" in datestring:
        date = today - relativedelta(minutes=intervalcount)
    if "hours" in datestring:
        date = today - relativedelta(hours=intervalcount)
    if "day" in datestring:
        date = today - relativedelta(days=intervalcount)
    if "today" in datestring:
        date = today
    if "yesterday" in datestring:
        date = today - relativedelta(days=1)
    if "week" in datestring:
        date = today - relativedelta(weeks=intervalcount)
    if "month" in datestring:
        date = today - relativedelta(months=intervalcount)
    if "year" in datestring:
        date = today - relativedelta(years=intervalcount)

    return date.isoformat()
