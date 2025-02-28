import dateparser
import scrapy
import re
import string

from tpdb.BaseSceneScraper import BaseSceneScraper


class SugarDaddyPornSpider(BaseSceneScraper):
    name = 'SugarDaddyPorn'
    network = 'Sugar Daddy Porn'
    parent = 'Sugar Daddy Porn'

    start_urls = [
        'https://www.sugardaddyporn.com'
    ]

    selector_map = {
        'title': '//h1/text()',
        'description': '//div[@class="about-video"]/p/text()',
        'performers': '//div[contains(@class,"justify-between")]//div[contains(@class,"models-links")]/a/text()',
        'date': '//meta[@property="og:video:release_date"]/@content',
        'date_formats': ['%Y-%m-%d'],
        'image': '//meta[@property="og:image"]/@content',
        'tags': '',
        'external_id': '.*\/(.*)$',
        'trailer': '',
        'pagination': '/videos/recent?page=%s'
    }

    def get_scenes(self, response):
        scenes = response.xpath('//div[@class="models-video"]/a/@href').getall()
        for scene in scenes:
            yield scrapy.Request(url=self.format_link(response, scene), callback=self.parse_scene)


    def get_title(self, response):
        title = self.process_xpath(response, self.get_selector_map('title')).get()
        if title:
            if re.search('rating: \d{1,2}\/\d{1,2} ', title.lower()):
                titlebare = re.search('rating: \d{1,2}\/\d{1,2} (.*)', title.lower()).group(1)
                if titlebare:
                    if re.search('^ - ', title.lower()):
                        titlebare = re.search('^ - (.*)', title.lower()).group(1)                   
                if titlebare:
                    titlebare = string.capwords(titlebare)
                    title = titlebare.strip()
                
            if title:
                return title.strip()

        return None

    def get_image(self, response):
        image = self.process_xpath(response, self.get_selector_map('image'))
        if image:
            image = self.get_from_regex(image.get(), 're_image')

            if image:
                image = image.replace(" ","%20")
                return self.format_link(response, image)

        return None
