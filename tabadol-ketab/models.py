import requests
from bs4 import BeautifulSoup
from validator_collection import is_not_empty
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from persiantools.jdatetime import JalaliDate
from humanize import intcomma

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

    def get_want_to_read_books_names(self, username):
        #request = requests.get(self.goodreads_want_to_read_books_url.format(username=username))
        options = Options()
        options.add_argument("--headless")  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
        driver.get(self.goodreads_want_to_read_books_url.format(username=username))
        Goodreads().scroll_down(driver)
        request_content = driver.page_source
        driver.close()
        soup = BeautifulSoup(request_content, features="lxml")
        books_element_body = soup.find("tbody", {"id": "booksBody"})
        if not is_not_empty(books_element_body):
            return []
        goodreads_books_elements = books_element_body.find_all("td", {"class": "title"})
        books = []
        for goodreads_book_element in goodreads_books_elements:
            book_title = goodreads_book_element.text
            for split_option in [":",";","؛",",","،"]:
                book_title = book_title.split(split_option)[0]
                
            book_title = book_title.replace("  ","")
            book_title = book_title.replace("\n","")
            book_title = book_title[6:]
            books.append(book_title)
        return books

    def scroll_down(self, driver, times=40):
        for i in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(0.4)
