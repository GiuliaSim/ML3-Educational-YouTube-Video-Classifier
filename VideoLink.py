import scrapy
class VideoLink(scrapy.Spider):
    name = 'videoLink'
    allow_domains = [
        'youtube.com'
        ]
    start_urls = [
        'https://www.youtube.com/watch?v=fF1exDY0ofs' 
    ]


    def parse(self, response):
        
        for i in response.css('div.content-wrapper'):
            yield {
                'id': i.css('a.content-link.spf-link.yt-uix-sessionlink::attr(href)').get(),
            }
