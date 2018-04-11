from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = 'http://futpedia.globo.com/campeonato/campeonato-brasileiro/{}'  # mudar ano p/ 2003
PREVIOUS_ROUND_XPATH = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[1]/div/span[1]'
MIN_YEAR = 2013
MAX_YEAR = 2014


class Navigator:
    def __init__(self):
        self._current_year = MIN_YEAR
        options = Options()
        options.add_argument("--headless")
        self._browser = webdriver.Chrome(chrome_options=options)
        self._browser = self.get_page(self.browser, BASE_URL.format(self._current_year))
        self.NUM_ROUNDS = self.__get_num_max_rounds()
        self._current_round = self.NUM_ROUNDS


    def __get_num_max_rounds(self):
        url = "http://futpedia.globo.com/campeonato/campeonato-brasileiro/{}".format(self.current_year)
        self._browser.get(url)
        num_rounds_xpath = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[1]/div/span[2]/span'
        data = self._browser.find_element_by_xpath(num_rounds_xpath).text

        return int(data[0:2])

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

    def to_next_round(self):
        self._browser.find_element_by_xpath(PREVIOUS_ROUND_XPATH).click()
        self._current_round -= 1

    def has_next_round(self):
        return self._current_round > 0

    def to_next_year(self):
        self._current_year += 1
        self._current_round = self.NUM_ROUNDS
        self._browser.get(BASE_URL.format(self._current_year))

    def has_next_year(self):
        return self._current_year < MAX_YEAR

    @property
    def current_year(self):
        return self._current_year

    @property
    def current_round(self):
        return self._current_round

    def quit(self):
        self._browser.quit()
