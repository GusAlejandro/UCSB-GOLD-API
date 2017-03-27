from settings import authentication
from selenium import webdriver


class Scraper:

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.searchPayload = None

    def get_webpage(self,url):
        self.browser.get(url)

    def login(self):
        self.get_webpage('https://my.sa.ucsb.edu/gold/Login.aspx')
        user = self.browser.find_element_by_name('ctl00$pageContent$userNameText')
        password = self.browser.find_element_by_name('ctl00$pageContent$passwordText')
        user.send_keys(authentication['username'])
        password.send_keys(authentication['password'])
        self.browser.find_element_by_name('ctl00$pageContent$loginButton').click()


    def parse_course_listings(self, raw_html):
        pass

    def get_course_listings(self, quarter, subject):
        self.login()
        self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        web = self.browser.page_source
        self.browser.close()
        return web

    def get_course_information(self, course):
        pass


