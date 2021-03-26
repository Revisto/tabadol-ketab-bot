import requests
from bs4 import BeautifulSoup
import setting

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
            books.append({"book_name": book_name, "book_details": book_details})
        
        return books
