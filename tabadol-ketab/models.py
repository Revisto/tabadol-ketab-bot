import requests
from bs4 import BeautifulSoup
import setting
from validator_collection import is_not_empty
from selenium import webdriver
from time import sleep
class TabadolKetab:
    def __init__(self):
        self.tabadol_ketab_search_url = "https://book.tabadolketab.com/searched?bookname={book_name}&motarjem=&moalef=&nasher=&categories=&conditionType=AND"

    def search_for_a_book(self, book_name):
        request = requests.get(self.tabadol_ketab_search_url.format(book_name=book_name))
        soup = BeautifulSoup(request.content, features="lxml")
        found_books_elements = soup.find_all("div", {"class": "tb-index-book"})
        books = []
        for book_element in found_books_elements:
            book_name = book_element.find("h3", {"class": "tb-book-title"}).text
            book_details = book_element.find("div", {"class": "tb-details-book"}).text
            book_details = book_details.replace("  ","")
            book_details = book_details.replace("\n","")
            book_details = book_details.replace("][","\n")
            book_details = book_details.replace("]","").replace("[","")
            book_details = f"{book_name}: \n\n\n {book_details}" 
            books.append({"book_name": book_name, "book_details": book_details})
        
        return books

    def search_for_books(self, book_names):
        books = []
        for book_name in book_names:
            tabadolketab_book_search_result = TabadolKetab().search_for_a_book(book_name)
            if is_not_empty(tabadolketab_book_search_result):
                books.append(book_name + " : " + tabadolketab_book_search_result[0]["book_name"])

        return books

class Goodreads:
    def __init__(self):
        self.goodreads_want_to_read_books_url = "https://www.goodreads.com/review/list/{username}?ref=nav_mybooks&shelf=to-read&per_page=100"

    def get_want_to_read_books_names(self, username):
        #request = requests.get(self.goodreads_want_to_read_books_url.format(username=username))
        driver = webdriver.PhantomJS()
        driver.get(self.goodreads_want_to_read_books_url.format(username=username))
        Goodreads().scroll_down(driver)
        request_content = driver.page_source
        soup = BeautifulSoup(request_content, features="lxml")
        books_element_body = soup.find("tbody", {"id": "booksBody"})
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

    def scroll_down(self, driver, times=10):
        for i in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1)

print (len(Goodreads().get_want_to_read_books_names("129432286-revisto")))