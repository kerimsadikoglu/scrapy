import scrapy


class TrendyolSpider(scrapy.Spider):
    name = "trendyol"
    allowed_domains = ["www.trendyol.com"]
    
    def start_requests(self):
        
        for i in range(1, 6):  # İlk 5 sayfa için URL oluştur
            url = f'https://www.trendyol.com/cep-telefonu-x-c103498?pi={i}'          
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.body)
        link_bas = "https://www.trendyol.com"
        telefonlar = response.xpath("//div[@class='p-card-wrppr with-campaign-view']")
        for telefon in telefonlar:
            # Diğer bilgileri çek
            telefon_adi = telefon.xpath(".//span[@class='prdct-desc-cntnr-name hasRatings']/text()").get()
            telefon_fiyat = telefon.xpath(".//div[@class='prc-box-dscntd']/text()").get()
            telefon_yildiz = None  # Varsa yıldız bilgisini de çekebilirsiniz
            telefon_yorum = telefon.xpath(".//span[@class='ratingCount']/text()").get()

            # Detay sayfasının linkini çek
            telefon_link_son = telefon.xpath(".//div[@class='p-card-chldrn-cntnr card-border']/a/@href").get()
            telefon_link = link_bas + telefon_link_son
            telefon_img = None
            # Detay sayfasına istek gönder
            yield{
                'telefonIisim': telefon_adi,
                'telefonFiyat': telefon_fiyat,
                'telefonYildiz': telefon_yildiz,
                'telefonImg' : telefon_img,
                'telefonLink' : telefon_link,
                'telefonYorum' : telefon_yorum
            }

    