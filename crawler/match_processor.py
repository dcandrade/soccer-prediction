def get_operations(year):
    if year < 2016:
        return [
            get_teams,
            get_score,
            get_schedule,
            get_location,
            get_statistics,
            get_arbiter,
            get_cards,
            get_coaches,
            get_player_list
        ]
    else:
        return [
            get_teams,
            get_score,
            get_schedule,
            get_location,
            get_statistics,
            get_cards,
            get_coaches,
            get_player_list
        ]


def get_year_and_round(match_page):
    data = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/div[1]/div[1]/a/span').text
    year = int(data[22:26])
    match_round = int(data[41:42])

    return {
        'year': year,
        'round': match_round
    }


def get_teams(match_page):
    home_team = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/a[1]/span[1]')
    away_team = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/a[2]/span[1]')

    return {
        'home_team': home_team.text,
        'away_team': away_team.text
    }


def get_score(match_page):
    home_team_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/span[1]').text
    away_team_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[1]/div/h1/span[3]').text

    return {
        'score': {
            'home_team': int(home_team_score),
            'away_team': int(away_team_score)
        }
    }


def get_schedule(match_page):
    info = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/time').text
    import re
    data = re.split('[,-]', info.strip())

    return {
        'schedule': {
            'day': data[0].strip(),
            'date': data[1].strip(),
            'time': data[2].strip()
        }
    }


def get_location(match_page):
    stadium = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/span/span[1]').text
    city = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[1]/span/span[2]/span').text

    return {
        'location': {
            'city': city,
            'stadium': stadium
        }
    }


def get_coaches(match_page):
    home_team_coach = match_page.find_element_by_xpath('//*[@id="escalacao-mandante"]/div/div/span/span[2]').text
    away_team_coach = match_page.find_element_by_xpath('//*[@id="escalacao-visitante"]/div/div/span/span[2]').text

    return {
        'coaches': {
            'home_team': home_team_coach,
            'away_team': away_team_coach
        }
    }


def get_statistics(match_page):
    num_matches = match_page.find_element_by_css_selector('.contexto span').get_property('innerHTML')
    try:
        num_matches_same_score = match_page.find_element_by_xpath('//*[@id="jogo"]/div/div[2]/div[3]/p/span[2]').text
    except:
        num_matches_same_score = 0
    num_draws = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[3]/div[2]/span[1]').text
    num_wins_away_team = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[2]/div[2]').text
    num_wins_home_team = match_page.find_element_by_xpath('//*[@id="mais-venceu"]/div/div[1]/div[2]').text
    home_team_goals = match_page.find_element_by_xpath('//*[@id="marcou-gols"]/div/div[1]/div[2]').text
    away_team_goals = match_page.find_element_by_xpath('//*[@id="marcou-gols"]/div/div[2]/div[2]').text

    return {
        'statistics': {
            'previous_matches': int(num_matches),
            'previous_draws': int(num_draws),
            'matches_same_score': int(num_matches_same_score),
            'wins_home_team': int(num_wins_home_team),
            'wins_away_team': int(num_wins_away_team),
            'goals_home_team': int(home_team_goals),
            'goals_away_team': int(away_team_goals)
        }
    }


def get_arbiter(match_page):
    name = match_page.find_element_by_css_selector('.nome-juiz').get_property('innerHTML')

    return {
        'arbiter': name
    }


def get_cards(match_page):
    cards = match_page.find_elements_by_xpath('//*[@id="scroll-cartoes"]/div/div[1]/ul/li')
    match_cards = []

    for card in cards:
        name = card.find_element_by_css_selector('.jogador').get_attribute('innerHTML')
        team = card.find_element_by_css_selector('.sigla-time').get_attribute('innerHTML')
        type = 'yellow'

        if 'cartao-CV' in card.get_property('innerHTML'):
            type = 'red'

        card = {
            'player': name,
            'type': type,
            'team': team
        }
        match_cards.append(card)

    return {
        'cards': match_cards
    }


def get_player_list(match_page):
    home_players = []
    away_players = []
    home_team_players = match_page.find_elements_by_xpath('//*[@id="escalacao-mandante"]/ul/li')
    away_team_players = match_page.find_elements_by_xpath('//*[@id="escalacao-visitante"]/ul/li')

    for home_player, away_player in zip(home_team_players, away_team_players):
        try:
            position, name = home_player.text.split('\n')
            home_players.append({
                'name': name,
                'position': position
            })
        except ValueError:
            pass

        try:
            position, name = away_player.text.split('\n')
            away_players.append({
                'name': name,
                'position': position
            })
        except ValueError:
            pass

    return {
        'players': {
            'home_team': home_players,
            'away_team': away_players
        }
    }
