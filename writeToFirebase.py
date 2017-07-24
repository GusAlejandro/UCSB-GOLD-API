import pyrebase
from settings import config, codes_for_subject
import goldScraper

firebase = pyrebase.initialize_app(config)
db = firebase.database()


test_run = ["PHYS","MATH","ASTRO","CMPSC"]

for subj in test_run:
    result = goldScraper.get_all_info_for_courses_in("SPRING2017",subj)
    # print(result)
    db.child("course-listing").child(str(subj)).set(result)