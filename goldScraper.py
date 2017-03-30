from settings import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup



class Scraper:

    def __init__(self, quarter, subject, course=None):
        self.raw_subject = subject
        self.quarter = codes_for_quarters[quarter]
        self.subject = codes_for_subject[subject]
        self.course = course
        self.browser = webdriver.Chrome()
        self.payload = {self.raw_subject: []}

    def get_webpage(self, url):
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
        current = ''
        soup = BeautifulSoup(raw_html, 'html.parser')
        courseList = soup.find_all("span",class_='tableheader')
        for course in courseList:
            course = str(course.text)
            for word in course.split():
                current += ' ' + word
            self.payload[self.raw_subject].append(current)
            current = ''


    def get_course_listings(self):
        # TODO: package response as JSON
        self.login()
        self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        quarterField = Select(self.browser.find_element_by_name('ctl00$pageContent$quarterDropDown'))
        quarterField.select_by_value(self.quarter)
        subjectField = Select(self.browser.find_element_by_name('ctl00$pageContent$subjectAreaDropDown'))
        subjectField.select_by_value(self.subject)
        self.browser.find_element_by_name('ctl00$pageContent$searchButton').click()
        text = self.browser.page_source
        self.browser.quit()
        self.parse_course_listings(text)
        self.browser.quit()
        return self.payload


    def get_course_information(self, course):
        pass


# functions below will be for the API available

def get_courses(quarter, subject):
    gold = Scraper(quarter, subject)
    response = gold.get_course_listings()
    return response

def get_course_info(quarter, subject, course):
    pass
