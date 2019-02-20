import scrapy
class VideoLink(scrapy.Spider):
    name = 'videoLink'
    allow_domains = [
        'youtube.com'
        ]
    api_url = 'https://www.youtube.com{}'
    start_urls = [
        api_url.format('/watch?v=ukzFI9rgwfU')
    ]
    maxVal = 5
    startVal = 0


    def parse(self, response):

        pages = []
        
        for i in response.css('div.content-wrapper'):
            page = i.css('a.content-link.spf-link.yt-uix-sessionlink::attr(href)').get()
            pages.append(page)
            yield {
                'id': page,
                'isEducational': '0',
            }

        if (self.startVal < self.maxVal):
            for i in range(len(pages)):
                next_page = pages[i]
                #self.logger.info(self.api_url.format(next_page))
                yield scrapy.Request(url=self.api_url.format(next_page), callback=self.parse)
                self.startVal = self.startVal + 1
