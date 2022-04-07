import requests
from bs4 import BeautifulSoup
from validator_collection import is_not_empty
from time import sleep
from persiantools.jdatetime import JalaliDate
from humanize import intcomma
from bs4 import BeautifulSoup
import math
import re

MONTH_NAMES_FA = [
    None,
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]

class TabadolKetab:
    def __init__(self):
        self.tabadol_ketab_search_url = "https://book.tabadolketab.com/v1/api/tabaadol-e-ketaab/books?filter[name]={book_name}"

    def search_for_a_book(self, book_name, update):
        results = requests.get(self.tabadol_ketab_search_url.format(book_name=book_name))
        results = results.json()
        books = []
        for book_sum in results["result"]["docs"][:10]:
            book_request = requests.get("https://book.tabadolketab.com/v1/api/tabaadol-e-ketaab/book/" + book_sum["id"]).json()
            book_name = book_request.get("name")
            book_category = (book_request.get("category")).get("title") if book_request.get("category") is not None else ""
            book_author = (book_request.get("author")).get("title") if book_request.get("author") is not None else ""
            book_publisher = (book_request.get("publisher")).get("title") if book_request.get("publisher") is not None else ""
            book_translator = (book_request.get("translator")).get("title") if book_request.get("translator") is not None else ""
            book_price = intcomma(int(book_request.get("afterDiscount"))/10)
            book_confirm_date = (book_request.get("confirmDate").split("T")[0]).split("-")
            book_confirm_date = str(JalaliDate.to_jalali(int(book_confirm_date[0]), int(book_confirm_date[1]), int(book_confirm_date[2]))).split("-")
            book_confirm_date_humanized = f"{book_confirm_date[2]} {MONTH_NAMES_FA[int(book_confirm_date[1])]} {book_confirm_date[0]}"
            book_details = f"""
نام کتاب: {book_name}


دسته بندی: {book_category}
نویسنده: {book_author}
مترجم: {book_translator}
ناشر: {book_publisher}
قیمت: {book_price}
تاریخ ورود: {book_confirm_date_humanized}
            """
            update.message.reply_text(book_details)
            books.append({"book_name": book_name, "book_details": book_details})
        
        return books

    def search_for_books(self, book_names):
        books = []
        for book_name in book_names:
            results = requests.get(self.tabadol_ketab_search_url.format(book_name=book_name))
            results = results.json()
            if is_not_empty(results["result"]["docs"]):
                books.append(book_name + " : " + results["result"]["docs"][0]["name"])

        return books

    def search_for_books_and_send_book_names_immediately(self, book_names, update):
        books = []
        for book_name in book_names:
            results = requests.get(self.tabadol_ketab_search_url.format(book_name=book_name))
            results = results.json()
            if is_not_empty(results["result"]["docs"]):
                books.append(book_name + " : " + results["result"]["docs"][0]["name"])
                telegram_bot(update).reply_text(books[-1])

        return books



class telegram_bot:
    def __init__(self, update):
        self.update = update
        
    def reply_text(self, message):
        self.update.message.reply_text(message)



class Goodreads:
    def __init__(self):
        self.goodreads_want_to_read_books_url = "https://www.goodreads.com/review/list/{username}?ref=nav_mybooks&shelf=to-read&per_page=infinite"

    def get_want_to_read_books_names(self, book_list_id):
        url = f"https://www.goodreads.com/review/list/{book_list_id}?page=1&shelf=to-read&utf8=✓&sort=date_read&order=d"

        # Make a GET request to fetch the raw HTML content
        html_content = requests.get(url).text

        # Parse the html content
        soup = BeautifulSoup(html_content, "lxml")

        books = soup.find("table", attrs={"id": "books"})
        books = books.tbody.find_all("tr")

        number_of_books_read = int(soup.find('span', attrs={"class": "h1Shelf"}).span.text.lstrip('(').rstrip(')'))
        number_of_pages = math.ceil(number_of_books_read/30)

        books = []
        for page in range(1, number_of_pages + 1):
            url = f"https://www.goodreads.com/review/list/{book_list_id}?page={page}&shelf=to-read&utf8=✓&sort=date_read&order=d"

            # Make a GET request to fetch the raw HTML content
            html_content = requests.get(url).text

            # Parse the html content
            soup = BeautifulSoup(html_content, "lxml")

            books = soup.find("table", attrs={"id": "books"})
            books = books.tbody.find_all("tr")

            for book in books:
                for td in book.find_all("td"):
                    row_name = td.label.text.replace('\n', ' ').strip()
                    if row_name == 'title':
                        book_title = td.div.text.replace('\n', ' ').strip()
                        book_title = book_title.replace('\u200c', ' ')
                        book_title = book_title.replace('\u202b', '')
                        book_title = re.sub("[\(\[].*?[\)\]]", "", book_title)
                        book_title = re.sub(' +', ' ', book_title)
                        for split_option in [":",";","؛",",","،"]:
                            book_title = book_title.split(split_option)[0]

                books.append(book_title)
        return books