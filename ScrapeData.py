import requests
import csv
from bs4 import BeautifulSoup
import re
from datetime import datetime
import numpy as np


def fetch_list():
    years = [i for i in range(2019, 2020)]
    pages = [0, 1]
    with open("imdb_data.csv", 'w', encoding="utf8", newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['imdb_id', 'name', 'imdb_rating', 'metascore',
                         'votes', 'genres', 'runtime', 'certificate', 'revenue'])
        for year in years:
            for page in pages:
                print('Fetching page '+str(page+1)+' for year '+str(year))
                request_url = 'https://www.imdb.com/search/title?title_type=feature&languages=en&countries=us&release_date=' + \
                    str(year)+'&count=250&start='+str((page*250)+1)
                response = requests.get(request_url)
                movies = BeautifulSoup(response.text, 'html.parser')
                elements = movies.find_all(
                    'div', class_='lister-item mode-advanced')
                for elem in elements:
                    nodes = elem.find_all('span', attrs={'name': 'nv'})
                    metascore = elem.find('div', class_='ratings-metascore')
                    if len(nodes) == 2 and metascore is not None:
                        imdb_id = elem.find('span', class_='userRatingValue')[
                            'data-tconst']
                        name = elem.h3.a.text
                        if elem.find('span', class_='runtime'):
                            runtime = int(
                                elem.find('span', class_='runtime').text.replace('min', ''))
                        genres = elem.find('span', class_='genre').text.strip()
                        metascore = elem.find(
                            'div', class_='ratings-metascore').span.text
                        cert = elem.find('span', class_='certificate')
                        if cert:
                            certificate = elem.find(
                                'span', class_='certificate').text
                        else:
                            certificate = 'Not Rated'
                        imdb_rating = float(elem.strong.text)
                        votes = int(nodes[0]['data-value'])
                        revenue = int(nodes[1]['data-value'].replace(',', ''))
                        writer.writerow(
                            [imdb_id, name, imdb_rating, metascore, votes, genres, runtime, certificate, revenue])


def fetch_budget(filename, filetype):
    print('Fetching Budget')
    with open(filename, 'r', encoding="utf8") as input_file, open(filetype+'_new.csv', 'w', encoding="utf8", newline='') as output_file:
        reader = csv.reader(input_file, delimiter=',')
        writer = csv.writer(output_file, delimiter=',')
        count = 0
        for row in reader:
            newrow = row
            if count == 0:
                newrow.append('budget')
                newrow.append('release_date')
                newrow.append('language')
                writer.writerow(newrow)
            else:
                movieObj = {}
                imdb_id = row[0]
                movieObj['imdb_id'] = imdb_id
                movie_data = requests.get(
                    "https://www.imdb.com/title/"+imdb_id+"/")
                soup = BeautifulSoup(movie_data.text, 'html.parser')
                for movie_detail in soup.find_all('h4'):
                    if "Budget:" in movie_detail:
                        movieObj['budget'] = movie_detail.next_sibling.strip()
                    elif "Language:" in movie_detail:
                        movieObj['language'] = movie_detail.next_sibling.next_element.text
                    elif "Cumulative Worldwide Gross:" in movie_detail:
                        movieObj['revenue'] = re.sub(
                            "[^0-9]", "", movie_detail.next_sibling.strip())
                    elif "Release Date:" in movie_detail:
                        try:
                            date_string = movie_detail.next_sibling.strip().split(" ")
                            if len(date_string) > 3:
                                date_str = date_string[0].strip(
                                )+' '+date_string[1].strip()+' '+date_string[2].strip()
                            else:
                                date_str = '01'+' ' + \
                                    date_string[0].strip()+' ' + \
                                    date_string[1].strip()
                            date_object = datetime.strptime(
                                date_str, '%d %B %Y')
                            movieObj['release_date'] = date_object.strftime(
                                "%Y-%m-%d")
                        except:
                            movieObj['release_date'] = np.nan
                if 'revenue' in movieObj.keys():
                    newrow[8] = movieObj['revenue']
                if 'budget' in movieObj.keys():
                    newrow.append(movieObj['budget'])
                else:
                    newrow.append(0)
                if 'release_date' in movieObj.keys():
                    newrow.append(movieObj['release_date'])
                if 'language' in movieObj.keys():
                    newrow.append(movieObj['language'])
                else:
                    newrow.append(np.nan)
                writer.writerow(newrow)
            count += 1
    print('Fetching Budget completed')


def convert_currency(curr, value):
    currency_list = {
        'KRW': 0.00085,
        'INR': 0.014,
        'JPY': 0.0092,
        'HUF': 0.0033,
        'EUR': 1.10,
        'GBP': 1.28,
        'CNY': 0.14,
        'CAD': 0.75,
        'AUD': 0.68,
        'SGD': 0.73,
        'SEK': 0.10,
        'NOK': 0.11,
        'THB': 0.033,
        'MXN': 0.052,
        'HKD': 0.13,
        'DKK': 0.15,
        'PLN': 0.26,
        'ISK': 0.0082
    }
    return currency_list[curr]*value


def update_budget(source, dest):
    with open(source, 'r', encoding="utf8") as input_file, open(dest, 'w', encoding="utf8", newline='') as output_file:
        reader = csv.reader(input_file, delimiter=',')
        writer = csv.writer(output_file, delimiter=',')
        count = 0
        for row in reader:
            newrow = row
            if count == 0:
                writer.writerow(newrow)
                pass
            else:
                budget = row[8]
                if budget[0].isdigit():
                    budget = re.sub("[^0-9]", "", budget.strip())
                elif budget[0] == '$':
                    budget = re.sub("[^0-9]", "", budget[1:].strip())
                else:
                    budget = convert_currency(budget[0:3], int(
                        re.sub("[^0-9]", "", budget[3:].strip())))
                newrow[8] = budget
                writer.writerow(newrow)
            count += 1


if __name__ == "__main__":
    fetch_list()
    fetch_budget('imdb_data.csv', 'imdb_data')
    update_budget('imdb_data_new.csv', 'final_imdb.csv')
