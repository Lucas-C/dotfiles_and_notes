import hashlib, os, scrapy

# List all HTML tags of a given type & their attributes on 1 or more web pages
# - input: a text file with 1 URL per line
# - output: a JSON file
# USAGE: scrapy runspider --pdb -L INFO $this_script.py -o $out.json -a tag_type=script -a urls_file=$input_file.txt

class MatchingTagFound(scrapy.Item):
    tag_name = scrapy.Field()
    url = scrapy.Field()
    text_md5 = scrapy.Field() # None => no text
    attributes = scrapy.Field()

class TagsCrawler(scrapy.Spider):
    name = os.path.basename(__file__)
    def __init__(self, tag_type, urls_file):
        assert tag_type and urls_file
        self.tag_type = tag_type
        self.start_urls = list(_read_urls_from_file(urls_file))
    def start_requests(self):
        # We only define this method because we can't log inside __init__ : http://stackoverflow.com/q/21785352
        self.log("Starting crawling {} web pages for html tag: '{}'".format(
            len(self.start_urls), self.tag_type), level=scrapy.log.INFO)
        return scrapy.Spider.start_requests(self)
    def parse(self, response):
        for tag in response.selector._root.xpath('//' + self.tag_type): # directly using lxml to get access to .items()
            yield MatchingTagFound(
                tag_name = self.tag_type,
                url = response.url,
                text_md5 = tag.text and hashlib.md5(tag.text.encode('utf-8')).hexdigest(),
                attributes = {k:v for (k,v) in tag.items()},
            )

def _read_urls_from_file(file_path):
    with open(file_path, "rb+") as open_file:
        for line in open_file.readlines():
            yield line.strip()

