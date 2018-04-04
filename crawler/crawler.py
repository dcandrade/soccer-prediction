from db.database import DAO
from crawler.navigation import Navigator

ROUND_RESULTS_SELECTOR = '.lista-de-jogos .jogos'
MATCH_RESULT_SELECTOR = '.lista-classificacao-jogo'
CLASSIFICATION_TABLE_XPATH = '//*[@id="edicao-campeonato-classificacao"]/div/div[2]/div[39]/div[1]/table/tbody'


class FutpediaCrawler:
    def __init__(self):
        self.navigator = Navigator()
        self.browser = self.navigator.get_browser()
        self.matches = []
        self.dao = DAO()

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
                'ano': self.navigator.current_year,
                'rodada': self.navigator.current_round,
                'time': entry.find_element_by_css_selector('.time').text,
                'pontos': int(entry.find_element_by_css_selector('.coluna-p').text),
                'jogos': int(entry.find_element_by_css_selector('.coluna-j').text),
                'vitorias': int(entry.find_element_by_css_selector('.coluna-v').text),
                'empates': int(entry.find_element_by_css_selector('.coluna-e').text),
                'derrotas': int(entry.find_element_by_css_selector('.coluna-d').text),
                'gp': int(entry.find_element_by_css_selector('.coluna-gp').text),
                'gc': int(entry.find_element_by_css_selector('.coluna-gc').text),
                'sg': int(entry.find_element_by_css_selector('.coluna-sg').text),
                'aproveitamento': float(entry.find_element_by_css_selector('.coluna-a').text)

            }
            self.dao.add_round_classification(round_result)

    def __process_matches(self):
        browser = self.navigator.browser
        for match_link in self.matches:
            browser.get(match_link)

    def run(self):
        print('Crawling process started')
        while self.navigator.has_next_year():
            while self.navigator.has_next_round():
                self.__collect_links_to_matches()
                self.__import_round_classification()
                self.navigator.to_next_round()
            print("Year #{} done".format(self.navigator.current_year))
            self.navigator.to_next_year()

        print('Done collecting matches and classifications. Now processing match pages')
        self.__process_matches()
