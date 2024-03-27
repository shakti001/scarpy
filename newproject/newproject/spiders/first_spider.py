import scrapy
import json

class ProxySpider(scrapy.Spider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    start_urls = ["https://www.yelp.nl/amsterdam"]


    def start_requests(self):
        api_key = 'stc6fcfnns9axth4fjm9'
        url = f'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all&user={api_key}'
        yield scrapy.Request(url=url, callback=self.parse_proxies)

    def parse_proxies(self, response):
        proxy_ips = response.text.splitlines()
        print(proxy_ips, "proxyipproxyipproxyip")
        for url in self.start_urls:
            print(url, "urlllllllllllllllllllllllllll")
            for proxy_ip in proxy_ips:
                yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': proxy_ip})

    def parse(self, response):
        print(response.body, "responseeeeeeeee2222222")
        # Extracting individual review elements
        reviews_container = response.css('div.css-p35y1s').getall()

        # reviews = response.xpath('//div[contains(@class, "review-content")]')
        print(reviews_container,"343434343434")
        for review in reviews_container:
            # Extracting review text
            review_text = review.xpath('.//p/text()').get()
            if review_text:
                yield {
                    'review': review_text.strip()
                }

        # Following pagination links
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)


