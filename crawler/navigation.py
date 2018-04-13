from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://futpedia.globo.com/campeonato/campeonato-brasileiro/{}'
PREVIOUS_ROUND_XPATH = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[1]/div/span[1]'
MIN_YEAR = 2003
MAX_YEAR = 2018


class Navigator:
    def __init__(self):
        self._current_year = MIN_YEAR
        options = Options()
        options.add_argument("--headless")
        self._browser = webdriver.Chrome(chrome_options=options)
        if self._current_year > 2016 or self._current_year == 2013:
            year_tag = str(self._current_year) + '-' + str(self._current_year)
            self.get_page(self._browser, BASE_URL.format(year_tag))
        else:
            self.get_page(self._browser, BASE_URL.format(self._current_year))
        self.NUM_ROUNDS = self.__get_num_max_rounds()

    def __get_num_max_rounds(self):
        if self._current_year < 2016:
            url = "http://futpedia.globo.com/campeonato/campeonato-brasileiro/{}".format(self.current_year)
            self._browser.get(url)
            num_rounds_xpath = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[1]/div/span[2]/span'
            data = self._browser.find_element_by_xpath(num_rounds_xpath).text

            return int(data[0:2])

        else:
            round_results = self.browser.find_element_by_xpath('//*[@id="edicao-campeonato"]/div[2]/div')

            raw_js_data = round_results.find_element_by_css_selector('script')
            raw_js_data = raw_js_data.get_property('innerHTML').replace('\n', '').strip()
            begin = raw_js_data.find('JOGOS: ') + len('JOGOS: ')
            end = raw_js_data.find('EQUIPES') - 2

            raw_data = raw_js_data[begin:end].strip()[:-1]

            import json
            data = json.loads(raw_data)
            rounds = []
            for game in data:
                rounds.append(game['rod'])

            return max(rounds)

    @property
    def browser(self):
        return self._browser

    def get_page(self, browser, match_url):
        browser.get(match_url)
        refreshes = 0
        while not self.is_page_available(browser):
            print('Page not found [#{}], retrying in 10s: {}'.format(refreshes, browser.current_url))
            sleep(10)
            browser.get(match_url)
            refreshes += 1
        return browser

    def is_page_available(self, browser):
        try:
            browser.find_element_by_css_selector('.endereco-404')
            return False
        except:
            return True

    def to_next_year(self):
        self._current_year += 1
        if self._current_year > 2016 or self._current_year == 2013:
            year_tag = str(self._current_year) + '-' + str(self._current_year)
            self._browser.get(BASE_URL.format(year_tag))
        else:
            self._browser.get(BASE_URL.format(self._current_year))

    def has_next_year(self):
        return self._current_year < MAX_YEAR

    @property
    def current_year(self):
        return self._current_year

    def quit(self):
        self._browser.quit()
