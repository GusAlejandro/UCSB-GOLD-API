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
        cur_course = None
        last_course = None
        lec_num = 1
        sec_num = 1
        # TODO: Make sure we hit all titles followed by associated tables of lectures and assorted info
        soup = BeautifulSoup(raw_html, 'html.parser')
        found = soup.find_all("table",width="585", align="left",cellpadding="0",border="0",cellspacing="0")
        for each in found:
            # this first part is to parse out course titles
            each = str(each)
            soup2 = BeautifulSoup(each,'html.parser')
            course_titles = soup2.find_all("span",class_="tableheader")
            if len(str(course_titles))>0:
                for course in course_titles:
                    lec_num = 1
                    # logic to collect course title, take from the other function
                    cur_course = course.text
                    cur_course = str(cur_course).replace(u'\xa0', u' ')
                    cur_course = cur_course.strip()
                    cur_course = " ".join(cur_course.split())
                    response[cur_course] = {"dummy" : "test"}
                    # print(course.text)
                    continue
            # next part is to check if its a lecture slot
            lectures = soup2.find_all("td",class_="clcellprimary",style="padding-right:3px;")
            if len(str(lectures))>0:
                count = True
                for lecture in lectures:
                    if count:
                        sec_num = 1
                        data = {}
                        #print(str(lecture))
                        parent_tag = lecture.parent
                        values = str(parent_tag.text).replace(u'\xa0', u' ')
                        values = values.split('\n')
                        data['days'] = str(values[2]).strip()
                        data['time'] = values[3]
                        temp = str(values[4]).strip()
                        data['instructor'] = " ".join(temp.split())
                        count = False
                        # print(data)
                        response[cur_course][lec_num] = data
                        # at this point data for a lecture is set
                        lec_num +=1
                        continue
            # here goes logic to check and see if we have a section block







            # print("===============================================================================")

        print(response)





    def get_course_listings(self):
        # TODO: package response as JSON before returning [CURRENTLY USING DICT IN RESPONSE, MAY NEED TO CHANGE TO GET JSON FORMAT]
        payload = self.parse_course_listings_for_title_only()
        return payload



    def get_course_information(self):
        # this is an function api call
        # print(courseTitles)
        self.parse_course_listings_for_lectures(self.raw_html)
        # # TODO: seperate going to course page as its own function
        # self.login()
        # self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        # quarterField = Select(self.browser.find_element_by_name('ctl00$pageContent$quarterDropDown'))
        # quarterField.select_by_value(self.quarter)
        # subjectField = Select(self.browser.find_element_by_name('ctl00$pageContent$subjectAreaDropDown'))
        # subjectField.select_by_value(self.subject)
        # self.browser.find_element_by_name('ctl00$pageContent$searchButton').click()
        # text = self.browser.page_source
        # self.browser.quit()
        # soup = BeautifulSoup(text, 'html.parser')
        # mainCourseList = soup.find_all("table",id="pageContent_CourseList") # captures the body of all courses
        # mainCourseList = str(mainCourseList)
        # mainCourseList = BeautifulSoup(mainCourseList, 'html.parser')
        # courseBlocks = mainCourseList.find_all("table", class_="datatable")
        # count = 0
        # tagForCourseInfo = "pageContent_CourseList_PrimarySections_"
        # current=''
        # for course in courseBlocks:
        #     # this gets each course block, now we need to get each ttile + lecture offering, within each course block
        #     course = str(course)
        #     courseSoup = BeautifulSoup(course, 'html.parser')
        #     # this gets the course title
        #     allCourseTitles = courseSoup.find_all("span",class_='tableheader')
        #     for courseTitle in allCourseTitles:
        #         courseTitle = str(courseTitle.text)
        #         for word in courseTitle.split():
        #             current += ' ' + word
        #         # TODO: at this point we have the title so here we do another evenNewSoup.find_all(lectures in course")
        #         print(current)
        #
        #         current = ''








# functions below will be for the API available

def get_course_titles_for(quarter, subject):
    # API call that returns all courses available for a particular subject in a given quarter
    gold = Scraper(quarter, subject)
    course_listings = gold.get_course_listings()
    return course_listings


def get_all_info_for_courses_in(quarter, subject):
    gold = Scraper(quarter,subject)
    response = gold.get_course_information()
    return response
