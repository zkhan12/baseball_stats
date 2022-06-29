'''
To use selenium you need to download chromedriver: https://www.swtestacademy.com/install-chrome-driver-on-mac/
then just pip install selenium
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import random

LOAD_TIME = 5  # Amount of seconds you want to wait for page to load, increase if loading is slow


# Convert input name to url name
def getName(nameStr):
    nameList = nameStr.split(' ')
    return str(nameList[1][:5] + nameList[0][:2]).lower()


# Build url
def getUrl(name, playerNumber, year):
    base = 'https://www.baseball-reference.com/players/split.fcgi?id={}{}&year={}&t=b'
    urlName = getName(name)
    return base.format(urlName, playerNumber, year)


# Load the page with selenium
def getPage(url):
    # Default options everyone uses with selenium, just ignore these
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)  # if your webdriver is saved in your downloads folder just specify the file path here
    driver.get(url)
    sleep(LOAD_TIME + random.random())  # let the page load
    page = driver.page_source
    driver.quit()
    return page


# Go to a page and get the table of season totals
def getTable(page):
    html = BeautifulSoup(page, 'html.parser')
    table = html.find('table', id='total')
    return pd.read_html(str(table))[0]


# Check until you get the right player that has correct year stats
def getValidTable(playerName, year, currentNumber):
    if currentNumber > 3:
        raise Exception("Player not found")
    formatCurrentNumber = '0{}'.format(str(currentNumber))
    url = getUrl(playerName, formatCurrentNumber, year)
    table = getTable(getPage(url))
    if table.loc[0, 'Split'].split(' ')[0] == str(year):
        return table
    currentNumber += 1
    return getValidTable(playerName, year, currentNumber)


# Return table
def getPlayerTotal(player, year):
    table = getValidTable(player, year, 1)
    return table


# Sample use case
print(getPlayerTotal('Jose Abreu', 2021))
