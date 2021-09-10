from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from django.shortcuts import render
import requests
import re
from concurrent.futures import ThreadPoolExecutor

# Create your views here.


#yahooニュース

    #requests
url = 'https://kabutan.jp/news/marketnews/?category=2&page=1'
res = requests.get(url)

#BeautifulSoup
soup = BeautifulSoup(res.content, 'html.parser')

#<a>タグの中からtext拾ってくる
elem = soup.find('a',href=re.compile('/news/marketnews/'),text=re.compile('任天堂'))
print(elem.parent.previous_sibling.previous_sibling.previous_sibling.text)