def get_year_and_match(match_page):
    data = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/div[1]/div[1]/a/span').text
    year = int(data[22:26])
    match_round = int(data[41:43])

    return year, match_round


def get_score(match_page):
    home_team = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/a[1]/span[1]').text
    home_team_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/span[1]')
    away_team = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/a[2]/span[1]').text
    away_team_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/span[3]')

    return [
        (home_team, home_team_score),
        (away_team, away_team_score)
    ]


def get_schedule(match_page):
    info = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/time').text
    import re
    data = re.split('[,-]', info.strip())
    return {
        'day': data[0].strip(),
        'date': data[1].strip(),
        'time': data[2].strip()
    }


def get_round(match_page):
    year = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/div[1]/div[1]/a/span/text()').text[-4:]
    return int(year)


def get_location(match_page):
    stadium = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/span/span[1]').text
    city = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/span/span[2]/span').text

    return {
        'city': city,
        'stadium': stadium
    }


def get_statistics(match_page):
    num_matches = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[3]/p/span[1]').text
    num_matches_same_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[3]/p/span[2]').text
    num_draws = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[3]/div[2]/span[1]').text
    num_wins_away_team = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[2]/div[2]').text
    num_wins_home_team = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[1]/div[2]').text
    home_team_goals = match_page.find_element_by_xpath('//*[@id="marcou-gols"]/div/div[1]/div[2]').text
    away_team_goals = match_page.find_element_by_xpath('//*[@id="marcou-gols"]/div/div[2]/div[2]').text

    return {
        'previous_matches': int(num_matches),
        'previous_draws': int(num_draws),
        'matches_same_score': int(num_matches_same_score),
        'wins_home_team': int(num_wins_home_team),
        'wins_away_team': int(num_wins_away_team),
        'goals_home_team': int(home_team_goals),
        'goals_away_team': int(away_team_goals)
    }


def get_arbiter(match_page):
    pass


def get_cards(match_page):
    pass

def get_players(match_page):
    pass