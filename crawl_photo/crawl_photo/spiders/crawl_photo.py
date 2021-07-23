import scrapy
from ..items import CrawlPhotoItem 

class spider1(scrapy.Spider):
    name = 'crawl_photo'
    def start_requests(self):
        urls = [
            'https://khodohoa.vn/tac-pham/nhiep-anh'
        ]
        for i in range(2, 47):
            urls.append('https://khodohoa.vn/tac-pham/nhiep-anh/page/' + str(i))
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        raw_image_urls = response.xpath('//img/@src').getall()
        clean_image_urls = []
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))

        yield {
            'image_urls' : clean_image_urls
        }