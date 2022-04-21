import requests
from validator_collection import is_not_empty
from persiantools.jdatetime import JalaliDate
from humanize import intcomma
import xml.etree.ElementTree as ET
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
            book_price = intcomma(int(int(book_request.get("afterDiscount"))/10))
            book_confirm_date = (book_request.get("confirmDate").split("T")[0]).split("-")
            try:
                book_confirm_date = str(JalaliDate.to_jalali(int(book_confirm_date[0]), int(book_confirm_date[1]), int(book_confirm_date[2]))).split("-")
                book_confirm_date_humanized = f"{book_confirm_date[2]} {MONTH_NAMES_FA[int(book_confirm_date[1])]} {book_confirm_date[0]}"
            except:
                book_confirm_date_humanized = "- - -"
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

    def get_want_to_read_books_names(self, GOODREADS_USERID, GOODREADS_KEY='XlkrscdJCPAF0m9mjtwFtA'):
        all_titles = []
        for page in range(1, 11):
            params = {
                'v': '2',
                'key': GOODREADS_KEY,
                'id': GOODREADS_USERID,
                'format': 'xml',
                'shelf': 'to-read',
                'per_page': '200',
                'page': str(page)
            }
            resp = requests.get('https://www.goodreads.com/review/list/' + GOODREADS_USERID, params=params)
            root = ET.fromstring(resp.content)

            books = root.findall('./reviews/review/book')
            titles = []
            for book_title in books:
                book_title = book_title.findall('./title')[0].text
                book_title = book_title.replace('\n', ' ').strip()
                book_title = book_title.replace('\u200c', ' ')
                book_title = book_title.replace('\u202b', '')
                book_title = re.sub("[\(\[].*?[\)\]]", "", book_title)
                book_title = re.sub(' +', ' ', book_title)
                for split_option in [":",";","؛",",","،"]:
                    book_title = book_title.split(split_option)[0]
                titles.append(book_title)
            if titles == []:
                break

            all_titles.extend(titles)
        return all_titles