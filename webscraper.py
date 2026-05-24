# i need to watch the price of this 4x4 apartment, because i heard it drops sometime in july or august lol
from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.palomawestmidtown.com/floor-plans/').text # uses http get request for the hmtl of the website
soup = BeautifulSoup(source, 'lxml')

four_bath_container = soup.select_one('div[data-beds="fourbed"][data-av-status="available"]') # searches for the fourbed that is available
if four_bath_container:
    clean_price = four_bath_container.get('data-price') # gets the price of the fourbed
    print(clean_price)