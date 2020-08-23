from selenium import webdriver, common
from path import Path
from bs4 import BeautifulSoup
import time
import pandas as pd


LINK_TO_DRIVER = Path('C:\chromedriver\chromedriver.exe')
driver = webdriver.Chrome(LINK_TO_DRIVER)
main_link = 'any_link'

driver.get(main_link)
YEARS = driver.find_element_by_css_selector('div.teamHeader__text')
years = YEARS.get_attribute('innerHTML').replace('/', '-')

for i in range(1, 4, 1):
    try:
        next_step = driver.find_elements_by_css_selector('a.event__more.event__more--static')
        next_step[-1].click()
        print('click ', i)
    except common.exceptions.ElementClickInterceptedException:
        print('exception')
        break


def get_table(elems):

    table = []
    for el in elems:
        html = el.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        date = soup.find('div', class_='event__time').get_text(strip=True)
        home_team = soup.find('div', class_='event__participant--home').get_text(strip=True)
        away_team = soup.find('div', class_='event__participant--away').get_text(strip=True)
        score = soup.find('div', class_='event__scores').get_text(strip=True)
        table.append({'years': years,
                      'date': date[:5].replace('.', '-'),
                      'home_team': home_team,
                      'away_team': away_team,
                      'score': score,
                      'total': int(score[0]) + int(score[2])})

    return table


elements = driver.find_elements_by_css_selector('div.event__match.event__match--static.event__match--oneLine')


def parse():

    table = get_table(elements)
    print('Table len ', len(table))
    print('Elements list len ', len(elements))
    if len(table) > 302:
        season_stat = pd.DataFrame(table)
        season_stat.to_csv(f'season_{years}_statistic.csv')


parse()

print('parsing finished')
time.sleep(5)
driver.close()
