from typing import Iterable
import scrapy
from scrapy.http import Request


class CepTelSpider(scrapy.Spider):
    name = "cep_tel"
    allowed_domains = ["www.amazon.com.tr"]
    start_urls = ["https://www.amazon.com.tr/s?rh=n%3A13709907031&fs=true&ref=lp_13709907031_sar"]
    current_page = 1

    def start_requests(self):
        yield scrapy.Request(url="https://www.amazon.com.tr/s?rh=n%3A13709907031&fs=true&ref=lp_13709907031_sar",callback=self.parse,headers=
                              {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        

    def parse(self, response):
        link_bas = "https://www.amazon.com.tr"
        telefonlar = response.xpath("//div[@class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']")
        for telefon in telefonlar:
            telefon_adi = telefon.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']/text()").get()
            telefon_fiyat = telefon.xpath(".//span[@class='a-price-whole']/text()").get()
            telefon_yildiz = telefon.xpath(".//i[@class='a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom']/span/text()").get()
            telefon_img = telefon.xpath(".//div[@class='a-section aok-relative s-image-square-aspect']/img/@src").get()
            telefon_link_son = telefon.xpath(".//a[@class='a-link-normal s-no-outline']/@href").get()
            
            telefon_link = link_bas + telefon_link_son
            telefon_yorum = telefon.xpath(".//span[@class='a-size-base s-underline-text']/text()").get()
            yield{
                'telefonIisim': telefon_adi,
                'telefonFiyat': telefon_fiyat,
                'telefonYildiz': telefon_yildiz,
                'telefonImg' : telefon_img,
                'telefonLink' : telefon_link,
                'telefonYorum' : telefon_yorum
            }
        next_page_son = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        next_page = link_bas + next_page_son
        if self.current_page < 5:
            self.current_page += 1
            next_page_son = response.xpath("//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href")
            if next_page_son:
                next_page = link_bas + next_page_son.get()
                yield scrapy.Request(url=next_page, callback=self.parse,headers=
                              {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})