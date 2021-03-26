import requests
import setting

class TabadolKetab:
    def __init__(self):
        self.tabadol_ketab_search_url = "https://book.tabadolketab.com/searched?bookname={book_name}&motarjem=&moalef=&nasher=&categories=&conditionType=AND"