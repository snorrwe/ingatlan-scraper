from lollygag import run, Services, LinkParser
from bs4 import BeautifulSoup
import requests


class MyRequests(object):

    USER_AGENT =\
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' + \
        ' AppleWebKit/537.36 (KHTML, like Gecko)' + \
        ' Chrome/63.0.3239.132 Safari/537.36'

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs, headers={
            'user-agent': MyRequests.USER_AGENT})


class IngatlanParser(LinkParser):

    def __init__(self, *args, **kwargs):
        super(IngatlanParser, self).__init__(*args, **kwargs)

    def feed(self, doc):
        soup = BeautifulSoup(doc, 'html.parser')
        cards = soup.find_all(class_='listing__card')

        for card in cards:
            price = card.findChildren(class_='price')[0].contents[0]
            area = card.findChildren(
                class_='listing__data--area-size')[0].contents[0]
            with open('results.csv', 'a+') as f:
                f.write("%s,%s\n" % (price, area))

        next_buttons = soup.find_all(
            class_='pagination__button')
        for btn in next_buttons:
            self.log_service.debug(btn['href'])
            self._links.add(btn['href'])


def main():
    with open('results.csv', 'w') as f:
        f.write('Price,Area\n')
    Services.site_parser_factory = IngatlanParser
    Services.requests = MyRequests
    run(url='https://ingatlan.com/lista/elado+lakas+xxii-ker')


if __name__ == '__main__':
    main()
