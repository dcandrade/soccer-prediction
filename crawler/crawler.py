from crawler import match_processor as mp
from db.database import DAO
from crawler.navigation import Navigator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CLASSIFICATION_TABLE_XPATH = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[39]/div[1]/table/tbody'


class FutpediaCrawler:
    def __init__(self):
        self.navigator = Navigator()
        self.browser = self.navigator.browser
        self.matches = []
        self.dao = DAO()
        options = Options()
        options.add_argument("--headless")
        self.__match_browser = webdriver.Chrome(chrome_options=options)

    def __collect_links_to_matches(self):
        self.matches.clear()
        round_results = self.browser.find_elements_by_xpath('//*[@id="lista-jogos"]/ul/li')
        for match in round_results:
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
        match_browser = self.__match_browser

        for count, match_url in enumerate(self.matches):
            len_round = len(self.matches) / self.navigator.NUM_ROUNDS
            match_round = int(count / len_round) + 1
            print("--- Processing match #{} of #{} : Round {} ".format(count + 1, len(self.matches), match_round))
            match_browser = self.navigator.get_page(match_browser, match_url)
            data = []

            for operation in mp.get_operations():
                data.append(operation(match_browser))

            match_data = {
                'url': match_url,
                'year': self.navigator.current_year,
                'round': match_round
            }

            for info in data:
                match_data.update(info)
            print("home: {}, {}".format(match_data['home_team'], match_url))
            self.dao.add_match(match_data)

    def run(self):
        try:
            print('Crawling process started')
            while self.navigator.has_next_year():
                print("Getting year #{}".format(self.navigator.current_year))
                self.__collect_links_to_matches()
                self.__process_matches()
                print("Year #{} done".format(self.navigator.current_year))
                self.navigator.to_next_year()
        except Exception as err:
            print(self.browser.current_url)
            print(self.__match_browser.current_url)
            raise err

        self.__match_browser.quit()
        self.navigator.quit()


if __name__ == "__main__":
    crawler = FutpediaCrawler()
    crawler.run()
