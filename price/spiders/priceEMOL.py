import scrapy
from price.items import PriceItem
from price.items import ImgData
from scrapy.http import Request

# To read from a csv file
import csv


class PriceemolSpider(scrapy.Spider):
    name = 'priceEMOL'
    allowed_domains = ['emol.com']
    start_urls = ['http://emol.com/']

    # This function helps us to scrape the whole content of the website
    # by following the starting URLs in a csv file.

    def start_requests(self):
        # Read main category URLs from a csv file

        with open("/home/wottan/PycharmProject/PriceScrappy/csvFiles/SpiderMainCategoryLinksEMOL.csv", "rU") as f:

            reader = csv.DictReader(f)

        for row in reader:
            url = row['url']

        # Change the page value incrementally to navigate through
        # the productlist
        # You can play with the range value according to maximum
        # product quantity, 30 pages to scrape as default

        link_urls = [url.format(i) for i in range(1, 30)]

        for link_url in link_urls:
            print(link_url)

        # Pass to each link containing products to parse_ product_pages function
        # with the gender metadata

        request = Request(link_url, callback=self.parse_product_pages, meta={'gender': row['gender']})

        yield request

    # This function scrapes the page with the help of xpath provided

    def parse_product_pages(self, response):
        item = PriceItem()

        # Get the HTML block where all the products are listed
        # <div> HTML element with the "product-list-item" class name

        content = response.xpath('//div[starts-with(@class,"product-list-item")]')

        # loop through the each <div> element in the content

        for product_content in content:
            image_urls = []

            # get the product details and populate the items
            item['productId'] = product_content.xpath('.//a/@data- id').extract_first()
            item['productName'] = product_content.xpath('.//img/@title').extract_first()
            item['priceSale'] = product_content.xpath('.//ins[@class="price-payable"] / text()').extract_first()
            item['priceOriginal'] = product_content.xpath('.//del[@class="price-psfx"] / text()').extract_first()
            if item['priceOriginal'] is None:
                item['priceOriginal'] = item['priceSale']

            item['imageLink'] = product_content.xpath('.//img/@ data - original').extract_first()

            item['productLink'] = "https://www.emol.com.tr" + product_content.xpath('.//a/@href').extract_first()

            image_urls.append(item['imageLink'])

            item['company'] = "EMOL"
            item['gender'] = response.meta['gender']

            if item['productId'] is None:
                break

            yield item

        # download the image contained in image_urls
            yield ImgData(image_urls=image_urls)

            def parse(self, response):
                pass
