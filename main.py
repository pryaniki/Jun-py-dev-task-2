import wikipedia
import requests
from bs4 import BeautifulSoup as BS


def read_page(url, counter):

    request = requests.get(url)
    if request.status_code != 200:
        print('Не удалось попасть на страницу')
        return False, {}

    html = BS(request.content, 'html.parser')
    url = None

    links = html.find(id="mw-pages").find_all("a")
    for link in links:
        if link.contents[0] == 'Следующая страница':
            url = 'https://ru.wikipedia.org/' + link.attrs['href']
            break

    for el in html.find(id="mw-pages").select('[class~=mw-category-group]'):
      char = el.h3.contents[0].upper()
      if char in counter.keys():
          counter[char] += len(el.ul.find_all("li"))
      else:
          url = None
          break

    return url, counter


def get_count_animals(url):

    letters = [(lambda c: chr(c))(i) for i in range(1040, 1072)]
    counter = {}
    for c in letters:
        counter[c] = 0
    url, counter = read_page(url, counter)

    while url:
        url, counter = read_page(url, counter)
    return counter


def main():
    url = 'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'
    counter = get_count_animals(url)
    for c in counter:
         print(f'{c}: {counter[c]}')


if __name__ == '__main__':
    main()