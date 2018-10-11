#!/usr/bin/env python3

# INSTALL: pip install beautifulsoup4 pyyaml requests

# To generate the required overblog-posts-with-dates.yaml file, I executed the following JS code in the web console on https://admin.over-blog.com/activity :
# $$('#root > div > div:nth-child(2) > div > div > div:nth-child(3) > div:nth-child(1) > div > div > div > div').map(e => {
#     if (e.childNodes[2].tagName === 'NOSCRIPT') { // This is an article
#         return '  "' + e.querySelector('div:nth-child(1) > div:nth-child(3) > span').textContent
#              + '": ' + e.querySelector('div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').href
#     } else { // This is a date
#         return e.querySelector('div:nth-child(2) > div:nth-child(1)').textContent + ' '
#              + e.querySelector('div:nth-child(2) > div:nth-child(2) > div:nth-child(2)').textContent + ':'
#     }
# })
# There were still a few URLs with the character … in it that I had to fix

import locale, os, requests, yaml
from collections import namedtuple
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse


BlogPost = namedtuple('_BlogPost', ('old_url', 'date'))

locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')  # in order to parse French months

CONTENT_DIR = Path('content')
CONTENT_DIR.mkdir(exist_ok=True)
CACHE_HTML_DIR = Path('posts-html-cache')
CACHE_HTML_DIR.mkdir(exist_ok=True)


def dl_file_and_convert_url(url, dest_dir):
    filename = url.split('/')[-1]
    (CONTENT_DIR / dest_dir).mkdir(exist_ok=True)
    local_file_path = CONTENT_DIR / dest_dir / filename
    if not local_file_path.exists():
        with open(local_file_path, 'wb+') as local_file:
            local_file.write(requests.get(url).content)
    return '{}/{}'.format(dest_dir, filename)

all_posts = []
with open('overblog-posts-with-dates.yaml') as all_posts_file:
    for day, posts in yaml.safe_load(all_posts_file).items():
        for hour, url in posts.items():
            blog_post = BlogPost(old_url=url, date=datetime.strptime('{} {}'.format(day, hour), '%d %B %Y %H:%M'))
            all_posts.append(blog_post)

for post in all_posts:
    url_end = unquote(urlparse(post.old_url).path.split('/')[-1])
    print('Processing', url_end)
    in_html_filepath = CACHE_HTML_DIR / url_end
    if not in_html_filepath.exists():
        with open(in_html_filepath, 'wb+') as post_html_file:
            post_html_file.write(requests.get(post.old_url).content)
    with open(in_html_filepath) as post_html_file:
        soup = BeautifulSoup(post_html_file, 'html.parser')
    item = soup.find(class_='item')
    title_section = item.find(class_='title')
    infos_section = title_section.find(class_='infos')
    subtitle = infos_section.string.strip()
    out_md_filename = post.date.strftime('%Y-%m-%d_%H-%M_') + url_end.split('.html')[0] + '.md'
    out_md_filepath = CONTENT_DIR / out_md_filename
    with open(out_md_filepath, 'w') as post_md_file:
        post_md_file.write('Title: {}\n'.format(title_section.find('h2').string))
        post_md_file.write('Slug: {}\n'.format(url_end.split('.html')[0]))
        post_md_file.write('Date: {}\n'.format(post.date.strftime('%Y-%m-%d %H:%M')))
        if 'par ' in subtitle:  # WARNING: French-specific
            post_md_file.write('Author: {}\n'.format(subtitle.split('par ')[1]))
        post_md_file.write('---\n')
        for ob_section in item.find_all(class_='ob-section'):
            classes = ob_section['class']
            if 'ob-section-file' in classes:
                link = ob_section.find('a')
                post_md_file.write('\n[{}]({})\n\n'.format(link.string.strip(), dl_file_and_convert_url(link['href'], dest_dir='files')))
                continue
            if not any(c in classes for c in ('ob-section-html', 'ob-section-text', 'ob-section-link', 'ob-section-video', 'ob-section-images')):
                raise RuntimeError('Unknown ob-section: {}'.format(classes))
            if 'ob-section-text' in classes:
                ob_section = ob_section.find(class_='ob-text')
            for img in ob_section.find_all('img'):
                update_parent_href = False
                # If there is a high-res picture linked to this img, we scrap it instead
                if img.parent.get('href', '').split('/')[-1] == img['src'].split('/')[-1]:
                    img['src'] = img.parent['href']
                    update_parent_href = True
                img['src'] = dl_file_and_convert_url(img['src'], dest_dir='images')
                if update_parent_href:
                    img.parent['href'] = img['src']
            for elem in ob_section.children:
                post_md_file.write(elem if isinstance(elem, str) else elem.prettify())
