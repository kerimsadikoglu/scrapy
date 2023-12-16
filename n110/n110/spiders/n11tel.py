import scrapy


class N11telSpider(scrapy.Spider):
    name = "n11tel"
    allowed_domains = ["www.n11.com"]
    start_urls = ["https://www.n11.com/telefon-ve-aksesuarlari/cep-telefonu"]

    def start_requests(self):
        base_url = "https://www.n11.com/telefon-ve-aksesuarlari/cep-telefonu"
        for i in range(1, 6): 
            url0 = f"{base_url}?pg={i}"
            yield scrapy.Request(url=url0, callback=self.parse, headers={
                'User-Agent': 'your-user-agent'})
  

    def parse(self, response):
        link_bas = "https://www.n11.com"
        telefonlar = response.xpath("//li[@class='column ']/div")
        for telefon in telefonlar:
            telefon_adi = telefon.xpath(".//h3[@class='productName']/text()").get()
            telefon_fiyat = telefon.xpath(".//span[@class='newPrice cPoint priceEventClick']/ins/text()").get()
            telefon_yildiz = None
            telefon_img = None
            telefon_link = telefon.xpath(".//span[@class='newPrice cPoint priceEventClick']/@data-href").get()
            
            #telefon_link = link_bas + telefon_link_son
            telefon_yorum = telefon.xpath(".//span[@class='ratingText']/text()").get()
            yield{
                'telefonIisim': telefon_adi,
                'telefonFiyat': telefon_fiyat,
                'telefonYildiz': telefon_yildiz,
                'telefonImg' : telefon_img,
                'telefonLink' : telefon_link,
                'telefonYorum' : telefon_yorum
            }
        