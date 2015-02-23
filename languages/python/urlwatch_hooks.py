"""
ln -s urlwatch_hooks.py ~/.urlwatch/lib/hooks.py
+ add URL(s) in ~/.urlwatch/urls.txt
+ check cached websites in ~/.urlwatch/cache/
+ configure task (cf. scheduling in notes.py) & mail
"""
import lxml.html
def filter(url, data):
    html_tree = lxml.html.fromstring(data)
    xc_ssd_availability = html_tree.xpath('//td[contains(., "XC SSD")]/following-sibling::td[5]/descendant::*/text()')
    if xc_ssd_availability:
        return xc_ssd_availability[0]
