from bs4 import BeautifulSoup
import requests
import csv

# Mini project, webscraper on example.com
# ************************************************
# https://www.youtube.com/watch?v=ng2o98k983k
# very helpful tutorial
# ************************************************

# Gets the heading and paragraphs and writes it to a csv
source = requests.get('https://example.com').text # uses http get request for the hmtl of the website
soup = BeautifulSoup(source, 'lxml')

# finds the body
body = soup.find('body')
# finds the heading and only takes the text
heading = body.find('h1').text
# for every paragraph element, we parse it and add it to a list
paragraphs = []
for paragraph in body.find_all('p'):
    paragraphs.append(paragraph.text)

# create dynamic headers, e.g. |title|paragraph1|paragraph2|paragraph3|etc
headers = ['title']
for i in range(len(paragraphs)):
    headers.append(f'paragraph{i+1}')

# combine the data into a single row
row_data = [heading] + paragraphs

# write to csv file
with open('example_scrape.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)
    csv_writer.writerow(row_data)