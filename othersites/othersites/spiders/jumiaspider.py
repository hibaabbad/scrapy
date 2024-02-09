import scrapy


class JumiaspiderSpider(scrapy.Spider):
    name = "jumiaspider"
    allowed_domains = ["www.jumia.com.dz"]
    start_urls = ["https://www.jumia.com.dz/mlp-ordinateurs-accessoires-informatique/ordinateurs-tablettes-ordinateurs-portables-traditionnels/"]
    

    def parse(self, response):
       products = response.css('article.prd').getall()
       for product in products:
           product_url = product.css('div.product-name a::attr(href)').get()
           yield scrapy.Request(product_url, callback=self.parse_pc_page)
