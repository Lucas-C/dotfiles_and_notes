import os, scrapy

# for f in page_*; do iconv -f WINDOWS-1252 -t utf8 $f | sed 's/charset=windows-1252/charset=utf-8/' > utf8_${f}l; done

# USAGE: rm out.json; scrapy runspider --pdb -L INFO $spider -o out.json; jq . out.json
#        scrapy runspider --pdb -L INFO $spider --set FEED_URI=venues.csv --set FEED_FORMAT=csv

HTML_FILES_PATH = 'file:///home/lucas/iMacros/Downloads/utf8_page_{i}.html'
BASE_SELECTOR = ('#fondcont > div > form > table'
                 '> tbody > tr > td > div > table'
                 '> tbody > tr:nth-child(4) > td > div > div > table > '
                 'tbody > tr:nth-child(4n+1)')

class Venue(scrapy.Item):
    name = scrapy.Field()
    subcategory = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    region = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    people = scrapy.Field()

class HtmlDirectoryCrawler(scrapy.Spider):
    name = os.path.basename(__file__)
    start_urls = [HTML_FILES_PATH.format(i=i * 25) for i in range(212)]

    def parse(self, response):
        for name_tr in response.css(BASE_SELECTOR):
            address_fields = name_tr.xpath('./following-sibling::tr[1]/td/table/tbody/tr[1]//text()').extract()
            contact_td = name_tr.xpath('./following-sibling::tr[1]/td/table/tbody/tr[2]/td')
            contact_div = contact_td.xpath('./div/text()').extract()
            if contact_div:
                address = contact_div[0]
                description = address_fields[1]
            else:
                address = address_fields[1]
                description = None
            phone_text = contact_td.xpath('./text()').extract()
            contact_fields = contact_td.xpath('./a/text()').extract()
            people = name_tr.xpath('./following-sibling::tr[3]/td/table/tbody/tr')
            people = [','.join(p.xpath('.//text()').extract()).replace(',', '') for p in people]
            yield Venue(name=str_clean(name_tr.css('td > a::text').extract()[0]),
                        subcategory=str_clean(name_tr.xpath('td[2]/text()').extract()[0]),
                        description=str_clean(description),
                        address=str_clean(address),
                        region=str_clean(address_fields[3]),
                        phone=str_clean(phone_text[0].strip().strip('-')) if phone_text else None,
                        email=str_clean(contact_fields[0]) if contact_fields else None,
                        website=str_clean(contact_fields[1]) if len(contact_fields) > 1 else None,
                        people=[str_clean(p) for p in people])

def str_clean(string):
    if not string:
        return string
    return string.encode('utf8').strip()
