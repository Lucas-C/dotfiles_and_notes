#!/usr/bin/python3

# Cram some French linguistic guides from fr.wikivoyage.org to be printed as compact PDFs
# (the export phase is not included, only some streamlined HTML files are produced)

# USAGE: ./wikivoyage_downloader.py
# REQUIRES: pip install beautifulsoup4 requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def process(src_url, sections_to_remove=()):
    dest_html_filepath = src_url.split('/')[-1] + '.html'
    base_url = '{0.scheme}://{0.netloc}'.format(urlparse(src_url))
    soup = BeautifulSoup(requests.get(src_url).text, 'html.parser')
    # mw-h2section / mw-h3section only exist after JS rendering, so some guessing is required to remove them:
    for headline_id in sections_to_remove:
        heading = soup.find(id=headline_id).parent
        current = heading.next_sibling
        heading.extract()
        while current and not (current.name and current.name in ('h2', 'h3')):
            bye = current
            current = current.next_sibling
            bye.extract()
    # We transform stylesheets URLs into absolute ones
    for link in soup.find_all('link'):
        if 'stylesheet' not in link['rel']:
            link.extract()
            continue
        if link['href'][:2] == '//':
            link['href'] = link['href'][2:]
        elif link['href'][0] == '/':
            link['href'] = base_url + link['href']
    for script in soup.find_all('script'):
        script.extract()
    for thumb in soup.find_all(class_='thumb'):
        thumb.extract()
    for img in soup.find_all('img'):
        img.extract()
    soup.find(id='mw-page-base').extract()
    soup.find(id='mw-head-base').extract()
    soup.find(id='mw-navigation').extract()
    soup.find(id='contentSub').extract()
    for noprint in soup.find_all(class_='noprint'):
        noprint.extract()
    if soup.find(class_='ext-wpb-pagebanner-subtitle'):
        soup.find(class_='ext-wpb-pagebanner-subtitle').extract()
    pre_content = soup.find(class_='pre-content')
    pre_content.insert_after(pre_content.find('h1'))
    pre_content.extract()
    soup.find(id='siteNotice').extract()
    soup.find(id='footer').extract()
    # We only allow the "Bases" section in the top right cartouche:
    allow_next_trs = False
    for tr in soup.find(class_='qb').find_all('tr'):
        if tr.get_text().strip() == 'Bases':
            allow_next_trs = True
            continue
        if allow_next_trs:
            if 'qbHeader' not in tr.td['class']:
                continue
            allow_next_trs = False
        tr.extract()
    # Some extra CSS to make the page more compact:
    extra_style = soup.new_tag('style')
    extra_style.string = '''
#content {
    margin-left: 0;
}
dl, p {
    column-rule: 1px solid;
}
dl {
    column-count: 5;
}
p {
    column-count: 2;
}
.prettytable {
    display: inline-block;
}'''
    soup.body.append(extra_style)
    with open(dest_html_filepath, 'w') as f:
        f.write(soup.prettify())


if __name__ == '__main__':
    process('https://fr.wikivoyage.org/wiki/Guide_linguistique_croate',
            sections_to_remove=('Voyelles', 'Consonnes', 'Liste_des_phrases', 'Achats', 'Conduire', 'Autorités', 'Approfondir'))
    process('https://fr.wikivoyage.org/wiki/Guide_linguistique_hongrois',
            sections_to_remove=('Voyelles', 'Consonnes', 'Grammaire', 'Achats', 'Conduite_automobile', 'Autorités', 'Approfondir'))
    process('https://fr.wikivoyage.org/wiki/Guide_linguistique_roumain',
            sections_to_remove=('Voyelles', 'Consonnes', 'Liste_des_phrases', 'Achats', 'Conduite_automobile', 'Autorités', 'Approfondir'))
    process('https://fr.wikivoyage.org/wiki/Guide_linguistique_serbe',
            sections_to_remove=('Voyelles', 'Consonnes', 'Achats', 'Conduite_automobile', 'Autorités', 'Approfondir'))
    process('https://fr.wikivoyage.org/wiki/Guide_linguistique_slovaque',
            sections_to_remove=('Voyelles_courte', 'Voyelles_longue', 'Consonne', 'Diphtongues', 'Grammaire', 'Principales_villes', 'Achats', 'Conduire', 'Autorité', 'Pays_et_langue', 'Approfondir', 'Dictionnaires'))
