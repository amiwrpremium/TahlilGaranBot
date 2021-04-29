import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
# TODO add profanity filter


class Dictionary:
    url = 'http://tahlilgaran.org/TDictionary/WebApp/'

    def user_search(self, word: str):
        params = {'q': word}

        r = requests.get(self.url, params=params)

        if r.status_code == 200:
            soup = bs(r.content, features='lxml')

            results = soup.find_all('div', attrs={'id': 'ResultDiv'})[0]

            if results.contents[0].name == 'a':
                self.word(results)
            else:
                self.index(results)

    @staticmethod
    def index(results: bs):
        print('index')
        result_contents = results.contents[1]

        dic = {}
        words = []
        status = []

        for x in result_contents:
            words.append(x.contents[0].text.strip())
            status.append(x.contents[1].text.strip())
            dic[x.contents[0].text.strip()] = x.contents[1].text.strip()

        print(dic)

    @staticmethod
    def word(results: bs):
        print('word')
        sections = results.find_all('a', attrs={'class': 'Tg_tb'})
        arr = []
        for x in sections:
            arr.append(x.get('name'))

        print(arr)

    def word_search(self, word):
        params = {'q': word}

        r = requests.get(self.url, params=params)

        if r.status_code == 200:
            soup = bs(r.content, features='lxml')

            results = soup.find_all('div', attrs={'id': 'ResultDiv'})[0]

    @staticmethod
    def pronounce_url(word: str):
        if word.startswith('O_'):
            _ = "O_uk_pron/n/nic/nice_/nice__gb_1"
            ox_dir = 'https://www.oxfordlearnersdictionaries.com/media/english/'
            return ox_dir + word[2:] + '.mp3'

        elif word.startswith("L_"):
            lo_dir = 'https://d27ucmmhxk51xv.cloudfront.net/media/english/exaProns/'
            return lo_dir + word[2:] + '.mp3?version=1.2.' + str(datetime.now().month + 17)

        elif word.startswith('C_'):
            co_dir = 'https://www.collinsdictionary.com/sounds/hwd_sounds/'
            return co_dir + word[2:] + '.mp3'
