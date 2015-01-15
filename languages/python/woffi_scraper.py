import os, scrapy

# USAGE: rm out.json; scrapy runspider --pdb -L INFO *.py -o out.json; jq . out.json
#        scrapy runspider --pdb -L INFO *.py --set FEED_URI=venues.csv --set FEED_FORMAT=csv

HTML_FILES_PATH = 'file:///home/lucas/iMacros/Downloads/page_{i}.htm'
BASE_SELECTOR = ('#fondcont > div > form > table'
                 '> tbody > tr > td > div > table'
                 '> tbody > tr:nth-child(4) > td > div > div > table > '
                 'tbody > tr:nth-child(4n+1)')

class Venue(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    region = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    people0 = scrapy.Field()
    people1 = scrapy.Field()
    people2 = scrapy.Field()
    people3 = scrapy.Field()
    people4 = scrapy.Field()
    people5 = scrapy.Field()
    people6 = scrapy.Field()
    people7 = scrapy.Field() # Yeah it's ugly, but I wasn't sure about how non-flat structure would be CSV-exported

class HtmlDirectoryCrawler(scrapy.Spider):
    name = os.path.basename(__file__)
    start_urls = [HTML_FILES_PATH.format(i=i * 25) for i in range(60)]

    def parse(self, response):
        for name_tr in response.css(BASE_SELECTOR):
            address_fields = name_tr.xpath('./following-sibling::tr[1]/td/table/tbody/tr[1]//text()').extract()
            contact_td = name_tr.xpath('./following-sibling::tr[1]/td/table/tbody/tr[2]/td')
            contact_div = contact_td.xpath('./div/text()').extract()
            if contact_div:
                address = contact_div[0].strip()
                description = address_fields[1].strip()
            else:
                address = address_fields[1].strip()
                description = None
            phone_text = contact_td.xpath('./text()').extract()
            contact_fields = contact_td.xpath('./a/text()').extract()
            people = name_tr.xpath('./following-sibling::tr[3]/td/table/tbody/tr')
            people = [','.join(p.xpath('.//text()').extract()).replace(',', '').strip() for p in people]
            assert len(people) <= 8
            yield Venue(name=name_tr.css('td > a::text').extract()[0].strip(),
                        description=description,
                        address=address,
                        region=address_fields[3].strip(),
                        phone=phone_text[0].strip().strip('-').strip() if phone_text else None,
                        email=contact_fields[0].strip() if contact_fields else None,
                        website=contact_fields[1].strip() if len(contact_fields) > 1 else None,
                        people0=people[0],
                        people1=people[1] if len(people) > 1 else None,
                        people2=people[2] if len(people) > 2 else None,
                        people3=people[3] if len(people) > 3 else None,
                        people4=people[4] if len(people) > 4 else None,
                        people5=people[5] if len(people) > 5 else None,
                        people6=people[6] if len(people) > 6 else None,
                        people7=people[7] if len(people) > 7 else None)
