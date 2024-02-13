import scrapy
from othersites.itemloaders import OthersitesLoader
from othersites.items import OthersitesItem

class LaoufispiderSpider(scrapy.Spider):
    name = "laoufispider"
    allowed_domains = ["laoufi.com"]
    start_urls = ["https://laoufi.com/categorie-produit/ordinateurs/"]

    def parse(self, response):
       products = response.css('ul.products li.product')
       for product in products:
           product_url = product.css('li.product a.woocommerce-LoopProduct-link::attr(href)').get()
           yield scrapy.Request(product_url, callback=self.parse_pc_page, meta={'product_url': product_url})
       
       
       # Get the next page URLs
       next_pages = response.css('ul.page-numbers li a::attr(href)').getall()
        # Follow each next page URL
       for next_page in next_pages:
            # Check if the URL is not None and has a scheme
            if next_page and '://' in next_page:
                yield response.follow(next_page, callback=self.parse)
            else:
                self.logger.warning(f"Ignoring invalid URL: {next_page}")
        
        
    def parse_pc_page(self, response):
        product_url = response.meta.get('product_url','')
        product = response.css('div.product')
        item = OthersitesLoader(item=OthersitesItem(), selector=product)
        item.add_css('name', "h1.product_title::text")
        item.add_value('url',product_url)
        item.add_css('photo',"figure div a::attr(href)")
        item.add_xpath('brand', "//div[@class='brand']/img/@alt")
        item.add_css('price',"p.price span span bdi::text")
        item.add_value('description',None)
        item.add_value('type',"Laptops"),
        item.add_value('source',"laoufi"),
        item.add_value('address',None),
        item.add_value('status',"New"),
        rows = response.css('table tr')
        for row in rows:
            characteristic_name = row.css('td strong::text').get()
            characteristic_value = row.css('td::text').get()

            if characteristic_name and characteristic_value:
                if characteristic_name.strip() == 'HDD':
                    item.add_value('disk', characteristic_value.strip())
                if characteristic_name.strip() == 'RAM':
                    item.add_value('ram', characteristic_value.strip())
                if characteristic_name.strip() == 'CPU':
                    item.add_value('cpu', characteristic_value.strip())
                if characteristic_name.strip() == 'ECRAN':
                    item.add_value('screen', characteristic_value.strip())
        yield item.load_item()
        
    def http_error_404(self, response, exception):
        self.logger.info(f"Ignoring 404 error for URL: {response.url}")
        pass