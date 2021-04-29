import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import re

# TODO add profanity filter


class Dictionary:
    url = 'http://tahlilgaran.org/TDictionary/WebApp/'
    pronounce_url_pattern = r'(?<=\(\')(.*?)(?=\'\))'

    def search(self, word: str, is_word_search: bool = False):
        if not is_word_search:
            params = {'q': word, 's': '1'}
        else:
            params = {'q': word}

        r = requests.get(self.url, params=params)

        if r.status_code == 200:
            soup = bs(r.content, features='lxml')

            results = soup.find_all('div', attrs={'id': 'ResultDiv'})[0]

            if results.contents[0].name == 'a':
                return self.word(results)
            else:
                return self.index(results)

    @staticmethod
    def index(results: bs):
        result_contents = results.contents[1]

        dic = {}
        words = []
        status = []

        for x in result_contents:
            words.append(x.contents[0].text.strip())
            status.append(x.contents[1].text.strip())
            dic[x.contents[0].text.strip()] = x.contents[1].text.strip()

        return 'index', dic, None, None

    def word(self, results: bs):
        uk, us = self.get_pronounce_url(results)
        sections = results.find_all('a', attrs={'class': 'Tg_tb'})
        arr = []
        for x in sections:
            arr.append(x.get('name'))

        return 'word', arr, uk, us

    def get_pronounce_url(self, results: bs):
        pronounce = results.find_all('p', attrs={'class': 'DivEnglishTitle'})[0].find_all('img')[1:]
        uk = re.findall(self.pronounce_url_pattern, pronounce[0]['onclick'])[0]
        us = re.findall(self.pronounce_url_pattern, pronounce[1]['onclick'])[0]

        _uk = self.pronounce_url(uk)
        _us = self.pronounce_url(us)

        return _uk, _us

    @staticmethod
    def pronounce_url(word: str):
        if word.startswith('O_'):
            ox_dir = 'https://www.oxfordlearnersdictionaries.com/media/english/'
            return ox_dir + word[2:] + '.mp3'

        elif word.startswith("L_"):
            lo_dir = 'https://d27ucmmhxk51xv.cloudfront.net/media/english/exaProns/'
            return lo_dir + word[2:] + '.mp3?version=1.2.' + str(datetime.now().month + 17)

        elif word.startswith('C_'):
            co_dir = 'https://www.collinsdictionary.com/sounds/hwd_sounds/'
            return co_dir + word[2:] + '.mp3'
