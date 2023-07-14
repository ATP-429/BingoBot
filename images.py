from bs4 import BeautifulSoup
from PIL import Image
from urllib.parse import unquote
import requests

level = 'N5'

f = open(f'{level}.txt', 'r')
for i, line in enumerate(f.readlines()):
    url = unquote(line).rstrip()
    #print(repr(url))
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    img_link = unquote(soup.find(id='header-image')['src']).rstrip()
    print(soup.find(id='header-image'))
    try:
        img_data = requests.get(img_link, headers=headers).content
        #print(img_link)
        img_f = open(f'{level}/{i+1}.png', 'wb')
        img_f.write(img_data)
        img_f.close()
    except:
        img_link = unquote(soup.find(id='header-image')['data-ezsrc']).rstrip()
        img_data = requests.get(img_link, headers=headers).content
        #print(img_link)
        img_f = open(f'{level}/{i+1}.png', 'wb')
        img_f.write(img_data)
        img_f.close()

f.close()