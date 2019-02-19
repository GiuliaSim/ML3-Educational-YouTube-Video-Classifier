import scrapy
class VideoLink(scrapy.Spider):
    name = 'videoLink'
    allow_domains = [
        'youtube.com'
        ]
    start_urls = [
        'https://www.youtube.com/' 
    ]


    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url),

        for i in response.css('items/ytd-compact-video-renderer.style-scope'):
            yield {
                'id': i.css('a::attr("href")').get(),
                'ciccia': 'cuccu'
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)