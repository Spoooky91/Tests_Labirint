import pytest
from pages.labirint import MainPage
import time

def test_check_input_symbols_in_search(web_browser):
    """ Проверка, что при вводе знаков поиск работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести несколько знаков:
    page.search = '%!*'
    page.search_run_button.click()

    # Проверяем, что в списоке нет найденных товаров:
    assert page.products_titles.count() == 0

    # Проверяем, что появилось сообщение, что ничего не найдено:
    assert page.msg_search_er.get_text() == "Мы ничего не нашли по вашему запросу! Что делать?"


def test_check_search_electronic_books(web_browser):
    """ Проверка, что поиск электронных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска другие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Убираем из результатов поиска бумажные книги, нажимаем на кнопку "Бумажные книги":
    page.without_paper_books_button.click()
    time.sleep(10)

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() >= 1

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books(web_browser):
    """ Проверка, что поиск бумажных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска электронные книги, нажимаем на кнопку "Электронные книги":
    page.without_electronic_books_button.click()

    # Убираем из результатов поиска прочие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg


def test_check_search_expected(web_browser):
    """ Проверка, что фильтр товаров со статусом "Ожидается" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Убираем из результатов поиска товары по предзаказу, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Убираем из результатов поиска товары в наличии, нажимаем на кнопку "В наличии":
    page.sort_products_by_type_in_stock_is.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_waiting.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'ожидается' in title.lower(), msg


def test_check_search_in_stock(web_browser):
    """ Проверка, что фильтр товаров "В наличии" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'краска'
    page.search_run_button.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Нет в продаже":
    page.sort_products_by_type_out_of_stock.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Ожидаются":
    page.sort_products_by_type_waiting.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60

    # Проверяем, что найдены товары, которые имеются в наличии, их можно положить в корзину:
    for title in page.products_in_stock.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'корзину' in title.lower(), msg


def test_check_search_electronic_books_another_way(web_browser):
    """ Проверка, что фильтр электронных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    time.sleep(10)

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books_another_way(web_browser):
    """ Проверка, что фильтр бумажных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Электронные книги":
    page.electronic_books.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg

def test_check_search_other_goods(web_browser):
    """ Проверка, что фильтр других товаров в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'ластик'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    page.show_button.scroll_to_element()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60


def test_check_search_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" работает. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles_large.count() >= 1


def test_check_button_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" ведет на нужную страницу. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь видит страницу с рекомендациями книг от редакции:
    assert page.page_title.get_text() == "Что почитать: выбор редакции"
    
    
    def test_check_input_symbols_in_search(web_browser):
    """ Проверка, что при вводе знаков поиск работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести несколько знаков:
    page.search = '%!*'
    page.search_run_button.click()

    # Проверяем, что в списоке нет найденных товаров:
    assert page.products_titles.count() == 0

    # Проверяем, что появилось сообщение, что ничего не найдено:
    assert page.msg_search_er.get_text() == "Мы ничего не нашли по вашему запросу! Что делать?"


def test_check_search_electronic_books(web_browser):
    """ Проверка, что поиск электронных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска другие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Убираем из результатов поиска бумажные книги, нажимаем на кнопку "Бумажные книги":
    page.without_paper_books_button.click()
    time.sleep(10)

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() >= 1

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books(web_browser):
    """ Проверка, что поиск бумажных книг работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Убираем из результатов поиска электронные книги, нажимаем на кнопку "Электронные книги":
    page.without_electronic_books_button.click()

    # Убираем из результатов поиска прочие товары, нажимаем на кнопку "Прочие товары":
    page.without_others_products_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg


def test_check_search_expected(web_browser):
    """ Проверка, что фильтр товаров со статусом "Ожидается" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'золото'
    page.search_run_button.click()

    # Убираем из результатов поиска товары по предзаказу, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Убираем из результатов поиска товары в наличии, нажимаем на кнопку "В наличии":
    page.sort_products_by_type_in_stock_is.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_waiting.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'ожидается' in title.lower(), msg


def test_check_search_in_stock(web_browser):
    """ Проверка, что фильтр товаров "В наличии" работает нормально. """

    page = MainPage(web_browser)

    page.search = 'краска'
    page.search_run_button.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Нет в продаже":
    page.sort_products_by_type_out_of_stock.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Ожидаются":
    page.sort_products_by_type_waiting.click()

    # Убираем из результатов поиска отсутствующие товары, нажимаем на кнопку "Предзаказ":
    page.sort_products_by_type_order.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60

    # Проверяем, что найдены товары, которые имеются в наличии, их можно положить в корзину:
    for title in page.products_in_stock.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'корзину' in title.lower(), msg


def test_check_search_electronic_books_another_way(web_browser):
    """ Проверка, что фильтр электронных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    time.sleep(10)

    # Проверяем, что найдены электронные книги:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' in title.lower(), msg


def test_check_search_paper_books_another_way(web_browser):
    """ Проверка, что фильтр бумажных книг в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'зима'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Электронные книги":
    page.electronic_books.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Другие товары":
    page.other_goods.click()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что в найденных книгах нет электронных:
    for title in page.products_types.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'электронная' not in title.lower(), msg

def test_check_search_other_goods(web_browser):
    """ Проверка, что фильтр других товаров в выпадающем меню работает нормально. """

    page = MainPage(web_browser)

    page.search = 'ластик'
    page.search_run_button.click()

    # Нажимаем на кнопку "ТИП ТОВАРА":
    page.product_type.click()

    # Отжимаем галочку в строке "Бумажные книги":
    page.paper_books.click()

    page.show_button.scroll_to_element()

    # Нажимаем на кнопку "Показать":
    page.show_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() == 60


def test_check_search_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" работает. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles_large.count() >= 1


def test_check_button_what_to_read(web_browser):
    """ Проверка, что кнопка "Что почитать: выбор редакции" ведет на нужную страницу. """

    page = MainPage(web_browser)

    page.what_to_read_button.click()

    # Проверяем, что пользователь видит страницу с рекомендациями книг от редакции:
    assert page.page_title.get_text() == "Что почитать: выбор редакции"
    
    
    
  def test_check_search_series_crystal_palace(web_browser):
    """ Проверка, что поиск товаров определенной серии работает правильно. """

    page = MainPage(web_browser)

    page.search = 'дворец'
    page.search_run_button.click()

    # Нажимаем на кнопку "Серии" в горизонтальном меню:
    page.product_series_button.click()

    # Нажимаем на название серии "Хрустальный дворец":
    page.product_part_button.click()

    # Проверяем, что пользователь видит список книг:
    assert page.products_titles.count() >= 1


def test_check_search_video(web_browser):
    """ Проверка, что фильтр списка видео по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'здоров'
    page.search_run_button.click()

    # Нажимаем на кнопку "Видео" в горизонтальном меню:
    page.video_button.click()

    # Проверяем, что пользователь может видеть список 25 видео, отобранных по заданному параметру поиска:
    assert page.video_products.count() == 25

    # проверяем, что в списке только названия видео со ссылками:
    for title in page.video_products.get_attribute('href'):
        msg = 'Wrong product in search "{}"'.format(title)
        assert title != '', msg


def test_check_search_themes(web_browser):
    """ Проверка, что фильтр Темы по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'кухня'
    page.search_run_button.click()

    # Нажимаем на кнопку "Темы" в горизонтальном меню:
    page.themes_button.click()

    # Проверяем, что пользователь может видеть список 6 тем, отобранных по заданному параметру поиска:
    assert page.themes_products.count() == 6

    # проверяем, что в списке названия тем со ссылками:
    for title in page.themes_products.get_attribute('href'):
        msg = 'Wrong product in search "{}"'.format(title)
        assert title != '', msg


def test_check_search_theme(web_browser):
    """ Проверка, что выбор определенной Темы по ключевому слову работает правильно. """

    page = MainPage(web_browser)

    page.search = 'кухня'
    page.search_run_button.click()

    # Нажимаем на кнопку "Темы" в горизонтальном меню:
    page.themes_button.click()

    # Нажимаем на название темы "Литературная кухня. Вкусные рецепты для любимых читателей":
    page.theme_button.click()

    # проверяем, что пользователь видит нужную страницу:
    # Тест не проходит, т.к. страница не найдена
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert 'литературная кухня' in title.lower(), msg
    
    def test_check_main_search(web_browser):
    """ Проверка, что основной поиск работает нормально. """

    page = MainPage(web_browser)

    page.search = 'осень'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() == 60

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осен' in title.lower(), msg


def test_check_main_exact_search(web_browser):
    """ Проверка, что точный поиск работает нормально. """

    page = MainPage(web_browser)

    page.search = 'осень в сокольниках'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осень в сокольниках' in title.lower(), msg


def test_check_wrong_input_in_search(web_browser):
    """ Проверка, что ввод с неправильной раскладки клавиатуры работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести «осень» с английской клавиатуры:
    page.search = 'jctym'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие книги:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert 'осен' in title.lower(), msg


def test_check_wrong_input(web_browser):
    """ Проверка, что поиск при вводе с орфографическими ошибками работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести «карамель» с тремя ошибками:
    page.search = 'коромиль'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список книг:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь видит страницу с результатами поиска:
    title = page.page_title.get_text()
    msg = 'Wrong product in search "{}"'.format(title)
    assert title == 'Все, что мы нашли в Лабиринте по запросу «карамель»', msg


def test_check_input_numbers_in_search(web_browser):
    """ Проверка, что при вводе цифр поиск работает нормально. """

    page = MainPage(web_browser)

    # Попробуйте ввести несколько цифр:
    page.search = '12399'
    page.search_run_button.click()

    # Проверяем, что пользователь может видеть список товаров:
    assert page.products_titles.count() >= 1

    # Проверяем, что пользователь нашел соответствующие товары:
    for title in page.products_titles.get_text():
        msg = 'Wrong product in search "{}"'.format(title)
        assert '12399' in title, msg

