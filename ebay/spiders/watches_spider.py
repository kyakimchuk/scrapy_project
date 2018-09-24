import scrapy


class WatchesSpider(scrapy.Spider):
    name = 'watches'
    start_urls = ['https://www.ebay.com/sch/i.html?_from=R40&_oac=1&_prodsch=1&_dmd=1&LH_BIN=1&_ipg=200&_nkw=watches&_dcat=31387&rt=nc&_mPrRngCbx=1&_udlo=400&_udhi']
    # start_urls = ['https://www.ebay.com/sch/i.html?_from=R40&_oac=1&_prodsch=1&_dmd=1&LH_BIN=1&_mPrRngCbx=1&_udlo=400&_udhi=&_nkw=watches&_ipg=25&rt=nc']
    def parse(self, response):
        # follow pagination links
        for href in response.xpath('//a[@class="gspr next"]/@href'):
            yield response.follow(href, self.parse)

        # follow links to wathes pages
        for href in response.css('h3.lvtitle a::attr(href)'):
            yield response.follow(href, self.parse_watches)

    def parse_watches(self, response):
        id_pos = response.url.find('?')
        id = response.url[id_pos+5:id_pos+17]
        img_url = False
        for url in response.xpath('//*[@class="app-filmstrip__image cc-image"]/@src').extract():
            img_name_pos = url.find('s-l')
            if img_name_pos != -1:
                img_url = url
                break
        if not img_url:
            for url in response.xpath('//img[contains(@class,"vi-image-gallery__image")]/@src').extract():
                img_name_pos = url.find('s-l')
                if img_name_pos != -1:
                    img_url = url
                    break
        if img_url:
            img_url = img_url[:img_name_pos+2]+"l1600.jpg"
        else:
            img_url = response.xpath('//img[contains(@class,"vi-image-gallery__image vi-image-gallery__image--absolute-center")]/@src').extract_first()
        yield {
            'id': id,
            'item_url': response.url, 
            'price': response.xpath('//h2[@class="display-price"]//text()').extract_first(),
            'image_urls': [img_url],
            'name': response.css('h1.product-title::text').extract_first().strip(),
        }