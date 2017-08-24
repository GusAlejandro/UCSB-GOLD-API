from settings import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, quarter, subject):
        """
        :param quarter: user requested quarter 
        :param subject: user requested subject
        :var raw_subject: Raw input, API defined, name for the subject 
        :var quarter: Actual string used for quarter in UCSB GOLD
        :var subject: Actual string used for quarter in UCSB GOLD
        :var label: label used for response purposes
        :var browser: browser instance we use for scraping
        :var raw_html: each scraper call goes to the course search page, inputs quarter and subject, returns the HTML of that page for parsing
        """
        self.raw_subject = subject
        self.quarter = codes_for_quarters[quarter]
        self.subject = codes_for_subject[subject]
        self.label = self.raw_subject + " " + quarter
        self.browser = webdriver.Chrome()
        self.raw_html = self.get_subject_raw_html()

    def get_webpage(self, url):
        # requests a url with the browser object
        self.browser.get(url)

    def login(self):
        # TODO: Implement try and catch to return error message in case of invalid login credentials
        self.get_webpage('https://my.sa.ucsb.edu/gold/Login.aspx')
        username = self.browser.find_element_by_name('ctl00$pageContent$userNameText')
        password = self.browser.find_element_by_name('ctl00$pageContent$passwordText')
        username.send_keys(authentication['username'])
        password.send_keys(authentication['password'])
        self.browser.find_element_by_name('ctl00$pageContent$loginButton').click()


    def format_title(self, raw_title):
        raw_title = str(raw_title.text)
        formated_title = ''
        for word in raw_title.split():
            formated_title += ' ' + word
        return formated_title


    def parse_course_offering_data(self, raw_html):
        values = str(raw_html.text).replace(u'\xa0', u' ').split('\n')
        days = values[2].strip().replace('.', '')
        time = values[3].replace('.', '')
        instructor = values[4].strip().replace('.', '')
        instructor = " ".join(instructor.split())
        return days, time, instructor

    def parse_section_offering_data(self, raw_html):
        values = str(raw_html.text).replace(u'\xa0', u' ').split('\n')
        days = values[3].strip().replace('.', '')
        time = values[4].replace('.', '')
        instructor = values[5].strip().replace('.', '')
        instructor = " ".join(instructor.split())
        return days, time, instructor

    def get_subject_raw_html(self):
        # returns raw html for specified subject and quarter
        self.login()
        self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        quarter_field = Select(self.browser.find_element_by_name('ctl00$pageContent$quarterDropDown'))
        quarter_field.select_by_value(self.quarter)
        subject_field = Select(self.browser.find_element_by_name('ctl00$pageContent$subjectAreaDropDown'))
        subject_field.select_by_value(self.subject)
        self.browser.find_element_by_name('ctl00$pageContent$searchButton').click()
        raw_html = self.browser.page_source
        self.browser.quit()
        return raw_html

    def create_offering_bundle(self, days, time, instructor):
        data = {}
        data["days"] = days
        data["time"] = time
        data["instructor"] = instructor
        data["sections"] = {}
        return data

    def create_section_bundle(self, days, time, instructor):
        data = {}
        data["days"] = days
        data["time"] = time
        data["instructor"] = instructor
        return data

    def parse_course_listings_for_title_only(self):
        # takes in raw_html from request and returns dictionary of course titles
        course_listings = {self.label: []}
        current_course_title = ''
        soup = BeautifulSoup(self.raw_html, 'html.parser')
        all_courses = soup.find_all("span",class_='tableheader')
        for course in all_courses:
            course = str(course.text)
            for word in course.split():
                current_course_title += ' ' + word
            course_listings[self.label].append(current_course_title)
            current_course_title = ''
        return course_listings






    def parse_course_listings_for_lectures(self, raw_html):
        response = {}
        soup = BeautifulSoup(raw_html, 'html.parser')
        courses = soup.find_all("table", class_="datatable", style="width:auto;")

        for course in courses:
            course = str(course)
            soup2 = BeautifulSoup(course,'html.parser')
            title_html = soup2.find("div", class_="fl")

            course_title = self.format_title(title_html)

            course_offering = soup2.find_all("table", width="585", cellpadding="0", cellspacing="0", align="left", border="0")
            section_id = 0
            offering_id = 0
            offering_data = {}
            # offering in this loop refers to either course or section as they are marked the same in the HTML
            for offering in course_offering:
                if "final" in offering.text:
                    # collect information for course offering
                    section_id = 0
                    offering_id += 1
                    offering = offering.contents[1] # closing in on actual relevant data
                    days, time, instructor = self.parse_course_offering_data(offering)
                    offering_data[offering_id] = self.create_offering_bundle(days, time, instructor)
                elif "final" not in offering.text and "course info" not in offering.text:
                    # collect information for a section offering
                    section_data = {}
                    section_id +=1
                    offering = offering.contents[1] # closing in on actual relevant data
                    days, time, instructor = self.parse_section_offering_data(offering)
                    section_data = self.create_section_bundle(days,time,instructor)
                    offering_data[offering_id]["sections"][section_id] = section_data

            response[course_title] = offering_data
        return response

    def get_course_listings(self):
        return self.parse_course_listings_for_title_only()



    def get_course_information(self):
        return self.parse_course_listings_for_lectures(self.raw_html)


# functions below will be for the API available

def get_course_titles_for(quarter, subject):
    # API call that returns all courses available for a particular subject in a given quarter
    gold = Scraper(quarter, subject)
    course_listings = gold.get_course_listings()
    return course_listings


def get_all_info_for_courses_in(quarter, subject):
    # API call that returns all courses and associated offerings and sectiosn for the given subject and quarter
    gold = Scraper(quarter,subject)
    response = gold.get_course_information()
    return response
