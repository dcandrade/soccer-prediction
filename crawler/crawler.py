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
        if self.navigator.current_year < 2016:
            round_results = self.browser.find_elements_by_xpath('//*[@id="lista-jogos"]/ul/li')
            for match in round_results:
                match_link = match.find_element_by_tag_name('a').get_property('href')
                self.matches.append(match_link)
        else:
            base_url = "http://futpedia.globo.com"
            round_results = self.browser.find_element_by_xpath('//*[@id="edicao-campeonato"]/div[2]/div')

            raw_js_data = round_results.find_element_by_css_selector('script')
            raw_js_data = raw_js_data.get_property('innerHTML').replace('\n', '').strip()
            begin = raw_js_data.find('JOGOS: ') + len('JOGOS: ')
            end = raw_js_data.find('EQUIPES') - 2

            raw_data = raw_js_data[begin:end].strip()[:-1]

            import json
            data = json.loads(raw_data)
            for game in data:
                self.matches.append(base_url + game['url'])
            self.matches.reverse()

    def __process_matches(self):
        match_browser = self.__match_browser

        for count, match_url in enumerate(self.matches):
            if count < 260:
                continue
            len_round = len(self.matches) / self.navigator.NUM_ROUNDS
            match_round = int(count / len_round) + 1
            print("--- Processing match #{} of #{} : Round {} ".format(count + 1, len(self.matches), match_round))
            match_browser = self.navigator.get_page(match_browser, match_url)
            data = []

            for operation in mp.get_operations(self.navigator.current_year):
                data.append(operation(match_browser))

            match_data = {
                'url': match_url,
                'year': self.navigator.current_year,
                'round': match_round
            }

            for info in data:
                match_data.update(info)
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
