from settings import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup


## TODO: PREVIOUSLY THOUGHT OF METHOD OF TABLE WIDTH 585 does not work, deeper layers have it. look into parent tag beautiful soup

class Scraper:

    def __init__(self, quarter, subject):
        self.raw_subject = subject
        self.quarter = codes_for_quarters[quarter]
        self.subject = codes_for_subject[subject]
        self.label = self.raw_subject + " " + quarter
        self.browser = webdriver.Chrome()
        self.payload = None
        self.fullLoad = {self.raw_subject: []}
        self.raw_html = self.get_subject_raw_html()

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

    def get_subject_raw_html(self):
        # returns raw html for specified subject and quarter
        self.login()
        self.get_webpage('https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx')
        quarterField = Select(self.browser.find_element_by_name('ctl00$pageContent$quarterDropDown'))
        quarterField.select_by_value(self.quarter)
        subjectField = Select(self.browser.find_element_by_name('ctl00$pageContent$subjectAreaDropDown'))
        subjectField.select_by_value(self.subject)
        self.browser.find_element_by_name('ctl00$pageContent$searchButton').click()
        text = self.browser.page_source
        self.browser.quit()
        return text


    def parse_course_listings_for_title(self, raw_html):
        # takes in raw_html returns dictionary of course titles
        payload = {self.label: []}
        current = ''
        soup = BeautifulSoup(raw_html, 'html.parser')
        courseList = soup.find_all("span",class_='tableheader')
        for course in courseList:
            course = str(course.text)
            for word in course.split():
                current += ' ' + word
            payload[self.label].append(current)
            current = ''
        return payload

    def get_course_listings(self):
        # this is an function api call that returns a structured payload of course titles based on quarter and subject
        # TODO: package response as JSON
        self.payload = self.parse_course_listings_for_title(self.raw_html)
        return self.payload

    def parse_course_listings_for_lectures(self, raw_html):
        # TODO: currently getting number of courses instead of number of lectures, not specified in
        soup = BeautifulSoup(raw_html, 'html.parser')
        allCourses =soup.find_all("table", class_="datatable")
        count = 0
        tagForCourseInfo = "pageContent_CourseList_PrimarySections_"
        print("THERE ARE THIS MANY COURSES: " + str(len(allCourses)))
        for course in allCourses:
            #print(course)
            print(count)
            tag = tagForCourseInfo+str(count)
            courseInfo = str(course)
            courseInfo = BeautifulSoup(courseInfo, "html.parser")
            courseInfo = courseInfo.find("table", id=tag)
            # # at this point we have a specific course, now we can do this again and count the numebr of table with=585 it has = # of lectures
            courseInfo = str(courseInfo)
            courseInfo = BeautifulSoup(courseInfo, "html.parser")
            courseInfo = courseInfo.find_all("table", width="585")
            # TODO: bfore goin into loop, throw all the ones with a different immediate parent
            # for each in courseInfo:
            #     print(each)
            #     print("THE CURRENT COUNT IS: " +str(count))
            count += 1
        #print(courseInfo)
        print("this is the lenght " + str(len(courseInfo)))


    def get_course_information(self):
        # this is an function api call
        courseTitles = self.parse_course_listings_for_title(self.raw_html)
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

def get_courses(quarter, subject):
    # this is the one that only does courses
    gold = Scraper(quarter, subject)
    response = gold.get_course_listings()
    return response


def get_course_info(quarter, subject):
    gold = Scraper(quarter,subject)
    response = gold.get_course_information()
    return response
