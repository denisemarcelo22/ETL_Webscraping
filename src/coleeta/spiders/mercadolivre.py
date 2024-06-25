import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    #allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        
        products = response.css('div.ui-search-result__content')

        for produtos in products:

            prices = produtos.css('span.andes-money-amount__fraction::text').getall()
            cents = produtos.css('span.andes-money-amount__cents::text').getall()

# BUSCA AS INFORMAÇÕESS REFERENTES AO PRODUTO DIRETO NO SITE
            yield {
            'brand' : produtos.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
            'name' : produtos.css('h2.ui-search-item__title::text').get(),
            'old_price_reais': prices[0] if len(prices) > 0 else None,
            'old_price_centavos': cents[0] if len(cents) > 0 else None,
            'new_price_reais': prices[0] if len(prices) > 0 else None,
            'new_price_centavos': cents[0] if len(cents) > 0 else None,
            'reviews_rating_number' : produtos.css('span.ui-search-reviews__rating-number::text').get(),
            'reviews_amount' : produtos.css('span.ui-search-reviews__amount::text').get()
            }
# NAVEGA PARA AS PRÓXIMAS PÁGINAS
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button- -next a::attr(href)').get()
            if next_page:
                self.page_count += 1
            yield scrapy.Request(url=next_page, callback = self.parse)
            