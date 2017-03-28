from settings import authentication
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.payload = {}

    def get_webpage(self,url):
        self.browser.get(url)

    def login(self):
        # TODO: Implement try and catch to return error message in case of invalid login credentials
        self.get_webpage('https://my.sa.ucsb.edu/gold/Login.aspx')
        user = self.browser.find_element_by_name('ctl00$pageContent$userNameText')
        password = self.browser.find_element_by_name('ctl00$pageContent$passwordText')
        user.send_keys(authentication['username'])
        password.send_keys(authentication['password'])
        self.browser.find_element_by_name('ctl00$pageContent$loginButton').click()



    def parse_course_listings(self, raw_html):
        # TODO: Efficiently parse each class and implement Json packaging for return
        soup = BeautifulSoup(raw_html, 'html.parser')
        a = soup.find_all("span",class_='tableheader')
        for x in a:
            x = str(x.text)
            print(x.split())


    def get_course_listings(self, quarter, subject):
        self.login()
        self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        quarterField = Select(self.browser.find_element_by_name('ctl00$pageContent$quarterDropDown'))
        quarterField.select_by_value(quarter)
        subjectField = Select(self.browser.find_element_by_name('ctl00$pageContent$subjectAreaDropDown'))
        subjectField.select_by_value(subject)
        self.browser.find_element_by_name('ctl00$pageContent$searchButton').click()
        text = self.browser.page_source
        self.browser.quit()
        self.parse_course_listings(text)
        self.browser.quit()



    def get_course_information(self, course):
        pass

it = Scraper()
it.get_course_listings('20171', 'EARTH')
