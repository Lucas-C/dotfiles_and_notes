from collections import Counter, OrderedDict
import json, os, scrapy, urlparse

# Recursively crawl through an Apache standard index HTML directory page, and list all files found in a JSON file
# USAGE: scrapy runspider --pdb -L INFO $this_script.py -o $out.json -a url=http://$directory_url

class FileUrl(scrapy.Item):
    url = scrapy.Field()

class HtmlDirectoryCrawler(scrapy.Spider):
    name = os.path.basename(__file__)
    def __init__(self, url=''):
        self.start_urls = [url]
        self.ext_counter = Counter()
    def parse(self, response):
        for href in response.xpath('//a/@href')[5:]:
        # Skipping the 5 first hrefs: Name, Last modified, Size, Description, Parent Folder
            child_url = urlparse.urljoin(response.url, href.extract())
            is_garbage = child_url.endswith('_fichiers/')
            if is_garbage:
                continue
            is_folder = (child_url[-1] == '/')
            if is_folder:
                yield scrapy.Request(child_url, self.parse)
            else:
                ext = child_url.split('.')[-1]
                self.ext_counter[ext] += 1
                yield FileUrl(url=child_url)
    def closed(self, reason):
        ordered_ext_counter = OrderedDict(sorted(
                self.ext_counter.iteritems(),
                key=lambda (k,v): (v,k)))
        self.log("Stats on extensions found:\n{}".format(
            json.dumps(ordered_ext_counter, indent=4)),
            level=scrapy.log.INFO)

