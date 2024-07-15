import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = 'https://www.sports.ru/basketball/club/%s/'


class Article:
    def __init__(self, title: str, link: str, image: str, text: str):
        self.__title = title
        self.__link = link
        self.__image = image
        self.__text = text


class PostParser:
    def __init__(self, slug: str):
        self.__link = BASE_URL % slug

    @staticmethod
    def get_soup(url: str) -> BeautifulSoup:
        """
        Метод делает из веб-страницы и возвращает объект BeautifulSoup для дальнейшего разбора.
        """
        return BeautifulSoup(requests.get(url).content, 'lxml')

    def get_five_min_freshness_posts(self):
        post_list_html: BeautifulSoup = self.get_soup(self.__link)
        post_links = [item.get('href') for item in post_list_html.body.find_all('a', 'short-text')][:5]

        result = {}
        for link in post_links:
            post_html: BeautifulSoup = self.get_soup(link)
            post_datetime = post_html.body.find('time').get('datetime')
            delta = datetime.now() - datetime.strptime(post_datetime, '%Y-%m-%d %H:%M:%S')
            if delta.total_seconds() < 5 * 60:
                post_title = post_html.body.find('h1', 'h1_size_tiny').text.strip()
                # post_text = post_html.body.find('div', 'news-item__content js-mediator-article').text.strip()
                message = (f'<b>{post_title}</b>\n'
                           f'{link}')
                result[post_datetime] = message

        return result


if __name__ == "__main__":
    content = PostParser('los-angeles-clippers')
    print(content.get_five_min_freshness_posts())
