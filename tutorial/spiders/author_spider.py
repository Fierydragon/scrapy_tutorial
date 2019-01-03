import scrapy

class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for a in response.css('.author + a'):
            yield response.follow(a, callback=self.parse_author)
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'author': extract_with_css('.author-title::text'),
            'born': extract_with_css('.author-born-date::text'),
            'description': extract_with_css('.author-description::text')
        }
