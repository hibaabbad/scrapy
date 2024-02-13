import scrapy
from othersites.itemloaders import OthersitesLoader
from othersites.items import OthersitesItem

class JumiaspiderSpider(scrapy.Spider):
    name = "jumiaspider"
    allowed_domains = ["www.jumia.com.dz"]
    start_urls = ["https://www.jumia.com.dz/mlp-ordinateurs-accessoires-informatique/ordinateurs-tablettes-ordinateurs-portables-traditionnels/"]
    

    def parse(self, response):

       products = response.css('article.prd')
       for product in products:
           product_url = 'https://www.jumia.com.dz' + product.css('a.core').attrib['href']
           yield scrapy.Request(product_url, callback=self.parse_pc_page, meta={'product_url': product_url})

    def parse_pc_page(self, response):
        product_url = response.meta.get('product_url','')
        product = response.css('main.-pvs')
        item = OthersitesLoader(item=OthersitesItem(), selector=product)
        item.add_css('name', "div.-pls h1::text")
        item.add_value('url',product_url)
        item.add_css('photo',"div.itm img::attr(data-src)")
        item.add_css('brand',"a._more::text")
        item.add_css('price',"div.df span::text")
        item.add_css('description',"div.markup p::text")
        item.add_value('type',"Laptops"),
        item.add_value('source',"jumia"),
        item.add_value('address',None),
        item.add_value('status',"New")
        
        
        # Extract the <ul> element
        ul_element = response.css('div.markup ul')
        # Extract text from each <li> element within the <ul>
        li_texts = ul_element.css('li::text').extract()
        # Perform your logic with the extracted text
        for li_text in li_texts:
            cleaned_li_text = li_text.strip()
            if 'disque' in cleaned_li_text.lower():
                item.add_value('disk',cleaned_li_text)
            elif 'ram' in cleaned_li_text.lower():
                item.add_value('ram',cleaned_li_text)
            elif ('processeur' in cleaned_li_text.lower()) or ('cpu' in cleaned_li_text.lower()) :  
                item.add_value('cpu',cleaned_li_text)
            elif 'ecran' in cleaned_li_text.lower():
                item.add_value('screen',cleaned_li_text)
        yield item.load_item()

      