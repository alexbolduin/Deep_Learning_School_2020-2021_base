from selenium import webdriver
from path import Path
from bs4 import BeautifulSoup

link_to_driver = Path('C:\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(link_to_driver)

driver.get('https://www.flashscore.com/football/england/premier-league-1989-1990/results/')

elements = driver.find_elements_by_class_name('event__match--static')

def get_table(elems):
    table = []
    for el in elems:
        html = el.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        date = soup.find('div', class_='event__time').get_text(strip=True)
        home_team = soup.find('div', class_='event__participant--home').get_text(strip=True)
        away_team = soup.find('div', class_='event__participant--away').get_text(strip=True)
        score = soup.find('div', class_='event__scores').get_text(strip=True)
        table.append({'date': date[:5].replace('.', '-'),
                      'home_team': home_team,
                      'away_team': away_team,
                      'score': score})

    return table

def parse():
    table = get_table(elements)
    print(table)

parse()

driver.close()