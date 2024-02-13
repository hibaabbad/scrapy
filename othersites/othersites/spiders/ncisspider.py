import scrapy
from othersites.itemloaders import OthersitesLoader
from othersites.items import OthersitesItem

class NcisspiderSpider(scrapy.Spider):
    name = "ncisspider"
    allowed_domains = ["www.ncis.dz"]
    start_urls = ["https://www.ncis.dz/categorie-produit/informatique/ordinateurs/ordinateurs-portables/"]

    def parse(self, response):

       products = response.css('ul.products')
       for product in products:
           product_url = product.css('li a::attr(href)').get()
           yield scrapy.Request(product_url, callback=self.parse_pc_page, meta={'product_url': product_url})
           
    def parse_pc_page(self, response):
        product_url = response.meta.get('product_url',''),
        product = response.css('div.mf-single-product'),
        item = OthersitesLoader(item=OthersitesItem(), selector=product),
        item.add_css('name', "h1.product_title::text"),
        item.add_value('url',product_url),
        item.add_css('photo',"figure div a::attr(href)"),
        item.add_css('brand',"li.meta-brand a::text"),
        item.add_css('price',""),
        item.add_css('description',""),
        item.add_value('type',"Laptops"),        
        item.add_value('source',"nciss"),
        item.add_value('status',"New")