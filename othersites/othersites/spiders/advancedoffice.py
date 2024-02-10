import scrapy
from othersites.itemloaders import OthersitesLoader
from othersites.items import OthersitesItem

class AdvancedofficeSpider(scrapy.Spider):
    name = "advancedoffice"
    allowed_domains = ["advancedoffice.dz"]
    start_urls = ["https://advancedoffice.dz/tous/technologie/ordinateurs-et-ecrans/ordinateurs-portables.html?dir=desc&order=price"]

    def parse(self, response):

       products = response.css('li.item')
       for product in products:
           product_url = product.css('div.product-name a::attr(href)').get()
           yield scrapy.Request(product_url, callback=self.parse_pc_page)
           
       next_pages = response.css('div.pagination li a::attr(href)').getall()
       for next_page in next_pages:
            if next_page and next_page != '#':
                # Check if the link corresponds to the current page
                is_current_page = 'current' in response.css(f'div.pagination li a[href="{next_page}"]::attr(class)').get(default='')
                if not is_current_page:
                    yield response.follow(next_page, callback=self.parse)
       
    def parse_pc_page(self, response):
        product = response.css('div.product-essential')
        item = OthersitesLoader(item=OthersitesItem(), selector=product)
        item.add_css('name', "div.product-name h1::text")
        item.add_css('url',"")
        item.add_css('photo',"div.product-image-zoom a::attr(href)")
        item.add_css('price', 'replace_this_with_actual_css_selector_for_price')
        item.add_css('description',"ul.breadcrumbs li.product span::text")
        item.add_css('type',"ul.breadcrumbs li:nth-last-child(2) span::text")
        rows = response.css('table tr')
        for row in rows:
            td1=row.css('td:first-child::text').get()
            td2_content = row.css('td:nth-child(2)::text').get()
            if td1=='Disque dur':
                item.add_css('disque',td2_content)
            elif td1=='Mémoire vive':
                item.add_css('ram',td2_content)
            elif td1=='Processeur':  
                item.add_css('cpu',td2_content)
            elif td1=='Marque':
                item.add_css('marque',td2_content)
            elif td1=='Ecran':
                item.add_css('ecran',td2_content)
        yield item.load_item()

      