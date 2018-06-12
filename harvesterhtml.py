#!/usr/bin/env python3

import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import browsercookie


if len(sys.argv) < 4:
    sys.exit("Not enough argument, usage: harvester novel_index_url start_chapter end_chapter")

cj = browsercookie.firefox()

headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
}
def get_page(url):
    try:
        with closing(get(url, headers=headers, cookies=cj, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
                
    except RequestException as e:
        log_error("Error during request to {0} : {1}".format(url,str(e)))
        return None
        
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
            
def log_error(e):
    print(e)
    
def get_subtitle(html):
    for p in html.select("p.novel_subtitle"):
        subtitle = (p.text)
    return subtitle
    
def novel_content(html):
    for div in html.select("div#novel_honbun"):
         content = div
    return content
    
def html_builder(title, html, ch):
    if ch == 1:
        prev_link = ""
    else:
        prev_link = '<a href="' + str(int(ch)-1).zfill(3) + '.html">Prev Chapter</a>'
    if ch == int(chx):
        next_link = ""
    else:
        next_link = '<a href="' + str(int(ch)+1).zfill(3) + '.html">Next Chapter</a>'
    contents = novel_content(html)
    html_str = """<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + title + """</title>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
<div class="container"> 
<div class="row">
<h1 class="text-center">""" + title + """</h1>
<hr>
<div class="xs-col-6 text-left">""" + prev_link + """</div>
<div class="xs-col-6 text-right">""" + next_link + """</div>
<hr>
""" + str(contents) + """
<hr>
<div class="xs-col-6 text-left">""" + prev_link + """</div>
<div class="xs-col-6 text-right">""" + next_link + """</div>
<hr>
</div>
</body>
</html>
"""
    return html_str

url = (sys.argv[1])
ch0 = (sys.argv[2])
chx = (sys.argv[3])

for ch in range(int(ch0), int(chx)+1):
    raw_html = get_page(url + str(ch))
    html = BeautifulSoup(raw_html, "html.parser")
    print("Downloading chapter " + str(ch) + " - " + html.title.string)
    with open(str(ch).zfill(3) + ".html", "w") as text_file:
        print(f"{html_builder(get_subtitle(html), html, ch)}", file=text_file)
    
