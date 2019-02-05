import requests
from bs4 import BeautifulSoup
import os.path

web_prefix = "http:"
site = "http://webaddress.com/link/to/webpage"
path = "D:\\Path\\to\\Folder\\Scrapped\\"

extension = ".xyz"
num_ignore_char = 0
#number of characters to remove from the start of the extracted url

def download_link(download_url, store_path):
    if os.path.exists(store_path):
        print("\t\t", store_path, " already exists. skipping it.")
        return  True
    with open(store_path, 'wb') as f:
        if 'http' not in download_url:
            # sometimes an image source can be relative
            # if it is provide the base url which also happens
            # to be the site variable atm.
            download_url = '{}{}'.format(web_prefix, download_url)
        r = requests.get(download_url)  # create HTTP response object
        f.write(r.content)
    return True

def get_urls(site):
    urls = []
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_links = soup.find_all("a")
    for link in all_links:
        if extension in link.get("href"):
            urls.append(link.get("href")[num_ignore_char:])
    return urls


urls = get_urls(site)
count = 0
total = len(urls)
for url in urls:
    filename = url.split('/')[-1]
    filename = path+filename
    print("{0}/{1}\t{2}\t{3}".format(count, total, url, filename))#, end='\r')
    count+=1
    if(not download_link(url, filename)):
        print("\t\tError downloading ", url, " into ", filename)