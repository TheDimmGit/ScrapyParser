import scrapy


class LivelibSpider(scrapy.Spider):
    name = 'livelib'
    allowed_domains = ['https://www.livelib.ru/books/top']
    start_urls = ['https://www.livelib.ru/books/top']

    def parse(self, response):
        for item in response.css('.block-border'):
            title = '.brow-book-name ::text'
            author = '.brow-book-author ::text'
            year = '.compact td::text'
            year_list = [i for i in item.css(year).getall() if str(i).isdigit()]
            rating = '.rating-value ::text'
            img = '.cover-wrapper img::attr(data-pagespeed-lazy-src)'
            link = 'a::attr(href)'
            yield {
                'title': item.css(title).get(),
                'author': item.css(author).get(),
                'year': year_list[0] if year_list else 'n/a',
                'rating': item.css(rating).get(),
                'img': item.css(img).get(),
                'link': 'https://www.livelib.ru'+str(item.css(link).extract_first()),
            }
