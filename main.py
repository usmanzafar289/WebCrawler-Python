import urllib.request
from urllib.parse import urlparse
import re
from datetime import date
from datetime import datetime, timedelta
import time, threading
import os
import matplotlib.pyplot as plt
import networkx as nx
import subprocess

def read_html(url):
    try:
        with urllib.request.urlopen(url) as response:
            try:
                encoding = response.info().get_param('charset', 'utf8')
                data = response.read().decode(encoding)
                return data
            except:
                return ''
    except:
        return ''

def get_urls(base_url, document, main_filename):
    urllist = []
    find_re = re.compile(r'\bhref\s*=\s*("[^"]*"|\'[^\']*\'|[^"\'<>=\s]+)')
    for match in find_re.finditer(document):
        url = match.group(1)
        if url[0] in "\"'":
            url = url.strip(url[0])
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme == parsed.netloc == '':
            url = urllib.parse.urljoin(base_url, url)

            if url not in lst:
                lst.append(url)
                new_main_filename = add_node(url)
                add_edge(main_filename, url)
                html = read_html(url)
                write_html_file(url, html)
                url_list = get_urls(url, html, new_main_filename)

            urllist.append(url)
    # return list(set(urllist))
    return lst

def write_html_file(url, html):
    today_date = date.today()
    url = url.replace("https://", "")
    url = url.replace("http://", "")
    path, filename = os.path.split(url)
    path = path.replace("/", "\\")
    save_path = os.getcwd() + '\\' + 'data\\' + str(today_date) + '\\' + path + '\\'
    if not os.path.exists(save_path):
        save_path = save_path.replace("?", "")
        os.makedirs(save_path)
    if len(filename) == 0:
        filename = str(datetime.now()).replace(" ", "").replace(":", "") + '.html'
    filename = filename.replace("?", "")
    completeName = os.path.join(save_path, filename)
    try:
        file1 = open(completeName, "w")
        file1.write(html)
        file1.close()
    except:
        return ''

def write_file(urls):
    today_date = date.today()
    dir = 'data/' + str(today_date) + '/'
    if not os.path.exists(dir):
        os.makedirs(dir)
    file = str(today_date) + '.txt'
    with open(dir + file, 'w') as f:
        for item in urls:
            f.write("%s\n" % item)

def read_file():
    yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    file_list_path = 'data/' + str(yesterday_date) + '/' + str(yesterday_date) + '.txt'
    data = []
    if os.path.exists(file_list_path):
        data = [line.strip() for line in open(file_list_path, 'r')]
    return data

def generate_graph():
    G = nx.Graph()

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    nx.draw(G, with_labels = True)
    today_date = date.today()
    dir = 'data/' + str(today_date) + '/'
    plt.savefig(dir + "network_graph.png")  # save as png
    plt.show()  # display

def add_node(url):
    path, filename = os.path.split(url)
    nodes.append(filename)
    return filename

def add_edge(main_filename, url):
    path, filename = os.path.split(url)
    tuple = (main_filename, filename)
    edges.append(tuple)

def WebCrawl():
    lst = read_file()
    main_html = read_html(main_url)
    if main_url not in lst:
        lst.append(main_url)
        main_filename = add_node(main_url)
        write_html_file(main_url, main_html)
    main_url_list = get_urls(main_url, main_html, main_filename)

    if len(main_url_list) != 0:
        write_file(main_url_list)

    generate_graph()

def Search():
    word_count = 0
    search_word = input("Please enter a word\n")
    print("Searching...")
    today_date = date.today()
    dir = 'data/' + str(today_date) + '/'
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            filepath = subdir + os.sep + file
            f = open(filepath, "r")
            try:
                data = f.read()
                ptags = re.findall(r'<\s*p[^>]*>(.*?)<\s*/\s*p>', data)

                for tag_text in ptags:
                    pos = tag_text.find(search_word)
                    while pos >= 0:  # we find an occurence
                        word_count += 1
                        pos += len(search_word)
                        pos = tag_text.find(search_word, pos)
            except:
                continue
    print('Occurances of word "' + str(search_word) + '": ' + str(word_count))

def Ping():
    print(time.ctime())

    parsed_uri = urlparse(main_url)
    result = '{uri.netloc}'.format(uri=parsed_uri)
    p = subprocess.Popen(["ping.exe", result], stdout=subprocess.PIPE)
    print(p.communicate()[0])

    threading.Timer(WAIT_SECONDS, Ping).start()

###### Main Program ######
#main_url = 'http://www.wpocean.com/tf/html/smartfolio/index-1.html'\
main_url = 'https://premiumlayers.net/demo/html/laboq/layout1/index.html'
WAIT_SECONDS = 10*60
lst = []
nodes = []
edges = []

value = input("Please enter a task number:\n 1. Crawl website\n 2. Search a string in website\n 3. Ping a website\n")
if int(value) is 1:
    WebCrawl()
elif int(value) is 2:
    Search()
elif int(value) is 3:
    Ping()
