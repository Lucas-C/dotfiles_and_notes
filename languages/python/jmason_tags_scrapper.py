from collections import Counter, OrderedDict
import json, os, scrapy

TAINT_URL = "http://taint.org/page/{page!s}"
MIN_TAGS_COUNT_TO_BE_DISPLAYED = 90

class TagsList(scrapy.Item):
    tags = scrapy.Field()

class WeblogCrawler(scrapy.Spider):
    name = os.path.basename(__file__)
    handle_httpstatus_list = [404]
    def __init__(self, url=''):
        self.current_page = 1
        self.start_urls = [TAINT_URL.format(page=self.current_page)]
        self.entries_without_tags_count = 0
        self.tag_counter = Counter()
    def parse(self, response):
        if response.status == 404:
            self.log("Stopping {} at page {} returning 404".format(
                    self.name, self.current_page), level=scrapy.log.INFO)
            return
        for div in response.xpath("//div[contains(@class,'post')]"):
            tags = []
            tag_links = div.xpath("div[@class='entry-utility']/span[@class='tag-links']/a/text()")
            if tag_links:
                tags = [tag.extract() for tag in tag_links]
            tags_p = div.xpath("div[@class='entry-content']//p[starts-with(text(), '(tags:')]")
            if tags_p:
                tags = tags_p.xpath('a/text()').extract()
            if tags:
                for tag in tags:
                    self.tag_counter[tag] += 1
                yield TagsList(tags=tags)
            else:
                self.entries_without_tags_count += 1
        self.current_page += 1
        yield scrapy.Request(TAINT_URL.format(page=self.current_page))
    def closed(self, reason):
        self.log("Entries without any tags: {}".format(self.entries_without_tags_count),
                level=scrapy.log.INFO)
        counted_tags_displayed = {tag:count for tag,count in self.tag_counter.iteritems()
                if count >= MIN_TAGS_COUNT_TO_BE_DISPLAYED}
        ordered_tag_counter = OrderedDict(sorted(
                counted_tags_displayed.iteritems(),
                key=lambda (k,v): (v,k)))
        self.log("Tags found with count > {}:\n{}".format(
                MIN_TAGS_COUNT_TO_BE_DISPLAYED, json.dumps(ordered_tag_counter, indent=4)),
                level=scrapy.log.INFO)

