import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class YelpSpider2(scrapy.Spider):
    name = 'yelp2'
    allowed_domains = ["yelp.com"]

    start_urls = ['https://www.yelp.com/biz/green-valley-landscaping-services-san-francisco']

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10  # Adjust as needed
            )

    def parse(self, response):
        # Extracting individual review elements
        print("o23232323")
        reviews = response.xpath('//div[@class="css-p35y1s"]')

        for review in reviews:
            # Extracting review text
            review_text = review.xpath('.//p/text()').get()

            if review_text:
                yield {
                    'review': review_text.strip()
                }

        # Following pagination links
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse,
                wait_time=10  # Adjust as needed
            )
