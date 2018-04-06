from crawler import match_processor as mp
from db.database import DAO
from crawler.navigation import Navigator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROUND_RESULTS_SELECTOR = '.lista-de-jogos .jogos'
MATCH_RESULT_SELECTOR = '.lista-classificacao-jogo'
CLASSIFICATION_TABLE_XPATH = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[39]/div[1]/table/tbody'


class FutpediaCrawler:
    def __init__(self):
        self.navigator = Navigator()
        self.browser = self.navigator.browser
        self.matches = []
        self.dao = DAO()
        options = Options()
        options.add_argument("--headless")
        self.match_browser = webdriver.Chrome(chrome_options=options)

    def __collect_links_to_matches(self):
        round_results = self.browser.find_element_by_css_selector(ROUND_RESULTS_SELECTOR)
        for match in round_results.find_elements_by_css_selector(MATCH_RESULT_SELECTOR):
            match_link = match.find_element_by_tag_name('a').get_property('href')
            self.matches.append(match_link)

    def __import_round_classification(self):
        classification_table = self.browser.find_element_by_xpath(CLASSIFICATION_TABLE_XPATH)
        entries = classification_table.find_elements_by_css_selector('tr')

        for entry in entries:
            round_result = {
                'year': self.navigator.current_year,
                'round': self.navigator.current_round,
                'team': entry.find_element_by_css_selector('.time').get_property('innerHTML'),
                'points': int(entry.find_element_by_css_selector('.coluna-p div').get_property('innerHTML')),
                'num_matches': int(entry.find_element_by_css_selector('.coluna-j div').get_property('innerHTML')),
                'num_wins': int(entry.find_element_by_css_selector('.coluna-v div').get_property('innerHTML')),
                'num_draws': int(entry.find_element_by_css_selector('.coluna-e div').get_property('innerHTML')),
                'num_defeats': int(entry.find_element_by_css_selector('.coluna-d div').get_property('innerHTML')),
                'gp': int(entry.find_element_by_css_selector('.coluna-gp div').get_property('innerHTML')),
                'gc': int(entry.find_element_by_css_selector('.coluna-gc div').get_property('innerHTML')),
                'sg': int(entry.find_element_by_css_selector('.coluna-sg div').get_property('innerHTML')),
                'win_rate': float(entry.find_element_by_css_selector('.coluna-a div').get_property('innerHTML'))

            }
            self.dao.add_round_classification(round_result)

    def __process_matches(self):
        match_browser = self.match_browser
        for count, match_url in enumerate(self.matches):
            print("--- Processing match #{} of #{}".format(count+1, len(self.matches)))
            browser = self.navigator.get_page(match_browser, match_url)
            data = []

            for operation in mp.get_operations():
                data.append(operation(browser))

            match_data = {'url': match_url}

            for match in data:
                match_data.update(match)

            self.dao.add_match(match_data)

        self.matches.clear()

    def run(self):
        try:
            print('Crawling process started')
            while self.navigator.has_next_year():
                print("Getting year #{}.".format(self.navigator.current_year))
                while self.navigator.has_next_round():
                    print("- Round #{}".format(self.navigator.current_round))
                    self.__collect_links_to_matches()
                    self.__import_round_classification()
                    self.__process_matches()
                    self.navigator.to_next_round()
                print("Year #{} done".format(self.navigator.current_year))
                self.navigator.to_next_year()
        except Exception as err:
            print(self.browser.current_url)
            print(self.match_browser.current_url)
            raise err
