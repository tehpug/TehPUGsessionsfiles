import scrapy


class RecipeExtractor(scrapy.Spider):
    name = 'irancook'
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
        'ITEM_PIPELINES': {
            # Activate the project pipeline by uncommenting 
            #  this line after creating your database
            
            # 'irancook.pipelines.IrancookPipeline': 300,
        }
    }

    def start_requests(self):
        _type = {
            0: 'main_course',
            1: 'appetizer',
            2: 'dessert'        
        }

        urls = [
                'https://irancook.ir/ghaza/',
                'https://irancook.ir/pishghaza/',
                'https://irancook.ir/cake-shirini/'
            ]
        for index, url in enumerate(urls):
            yield scrapy.Request(
                                    url,
                                    callback=self.parse,
                                    dont_filter=True,
                                    meta={'type': _type[index]}
                                )

    def parse(self, response):
        food_link = response.xpath('//h3[@class="entry-title"]/a/@href').extract()
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()

        for food in food_link:
            yield scrapy.Request(
                                    food, 
                                    callback=self.parse_ingredient, 
                                    dont_filter=True,
                                    meta={'type': response.meta['type']}
                                )

        if next_page:
            yield scrapy.Request(
                                    next_page,
                                    callback=self.parse,
                                    dont_filter=True,
                                    meta={'type': response.meta['type']}
                                )


    def parse_ingredient(self, response):
        title = response.xpath('//h1/text()').extract_first()
        food_image = response.xpath('//section[@class="slider print-only"]//img/@src').extract_first()
        ingredient = response.xpath('//ul[@class="ingre"]/li[@itemprop="ingredients"]/text()').extract()
        recipe = response.xpath('//div[@itemprop="description"]//text()').extract()

        recipe_string = ' '.join(recipe)
        ingredients_string = '\n'.join(ingredient)
        yield {
            'food_type': response.meta['type'],
            'food_url': response.url,
            'food_id': int(response.url.split('/')[-2]),
            'food_name': title,
            'food_image': food_image,
            'ingredients': ingredients_string,
            'recipe': recipe_string\
                                    .replace('\xa0', ' ')\
                                    .replace('\n', '')\
                                    .replace('\r', '')\
                                    .replace('\u200c', ' ')\
                                    .replace('  ',' ').strip()
        }
