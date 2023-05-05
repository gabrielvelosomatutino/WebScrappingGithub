import requests
from requests.exceptions import HTTPError


def crawl_website(url: str) -> str:

  try:
    resposta = requests.get(url)
    resposta.raise_for_status()
  except HTTPError as exc:
    print(exc)
  else:
    return resposta.text

URL = 'https://www.github.com/trending/'

github = crawl_website(url=URL)
with open(file='github.html', mode='w', encoding='utf8') as arquivo:
  arquivo.write(github)


from bs4 import BeautifulSoup 
soup = BeautifulSoup(open('github.html', mode='r'), 'html.parser')

texto = soup.get_text()

tabela = soup.find_all('article')

ranking = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
nome = []
language = []
stars = []
forks = []
star_today = []

for item in tabela:
  nome.append(item.find('h1', {'class': "h3 lh-condensed"}).get_text().strip().replace('\n', '').replace(' ', ''))
  try:
    language.append(item.find('span', {'itemprop': "programmingLanguage"}).get_text().strip())
  except AttributeError:
    language.append('no language')

  conjunto = item.find_all('a', {'class': 'Link--muted d-inline-block mr-3'})
  stars.append(conjunto[0].get_text().strip())
  forks.append(conjunto[1].get_text().strip())
  star_today.append(item.find('span', {'class': 'd-inline-block float-sm-right'}).get_text().strip().replace(' stars today', ''))

nome = nome[0:10]
language = language[0:10]
stars = stars[0:10]
forks = forks[0:10]
star_today = star_today[0:10]

print(ranking)
print(nome)
print(language)
print(stars)
print(forks)
print(star_today)


import csv

with open(file='./github.csv', mode='w', encoding='utf8') as f:
  escritor_csv = csv.writer(f, delimiter=';')
  escritor_csv.writerow(['ranking', 'nome', 'language', 'stars', 'forks', 'star_today'])
  escritor_csv.writerows(list(map(lambda ranking, nome, language, stars, forks, star_today: [ranking, nome, language, stars, forks, star_today], ranking, nome, language, stars, forks, star_today)))