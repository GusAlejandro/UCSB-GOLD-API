# UCSB-GOLD-API
API to interface with GOLD, the course registration system at UC Santa Barbara. Can either setup REST endpoint w/Flask or simply use API. In order to use it, write in your login credentials into settings.py. This is not an official API from UCSB, just a side project of mine.

## Current Developments
* Mobile course planner app that uses this API
* Functionality to interact with GOLD
* Sample usage as REST API in flask
* Actual REST API service to retrieve data as alternative to scraping GOLD via this API


## API

### REST Endpoint (NOT OPERATIONAL)
Simply run endpoint.py, and curl. Example:
```
curl http://127.0.0.1:5000/goldapi/quarter/subject
```

This will return the list of courses given a particular quarter.

### API calls
### get_course_titles_for(quarter,subject)
Returns list of courses given a particular quarter and subject

### get_all_info_for_courses_in(quarter, subject)
Returns list of courses and its course offerings, along with the sections for each course offering, given a quarter and a subject


## Codes for Quarters and Course Subjects 

### Quarters
* Summer 2017 -> 'SUMMER2017'
* Spring 2017 -> 'SPRING2017'
* Winter 2017 -> 'WINTER2017'
* Fall 2016 -> 'FALL2016'
* Spring 2016 -> 'SPRING2016'
* Winter 2016 -> 'WINTER2016'
* Fall 2015 -> 'FALL2015'
* Summer 2015 -> 'SUMMER2015'
* Spring 2015 -> 'SPRING2015'
* Winter 2015 -> 'WINTER2015'
* Fall 2014 -> 'FALL2014'

### Course Subjects 
* Anthropology -> 'ANTH'
* Art -> 'ART'
* Art History -> 'ARTHI'
* Art Studio -> 'ARTST'
* Asian American Studies -> 'ASAM'
* Astronomy -> 'ASTRO'
* Biology -> 'BIO'
* Biomolecular Science and Engineering -> 'BMSE'
* Black Studies -> 'BLST'
* Chemical Engineering -> 'CHEMENG'
* Chemistry and Biochemistry -> 'CHEMBIO'
* Chicano Studies -> 'CHST'
* Chinese -> 'CHIN'
* Classics -> 'CLASS'
* Communication -> 'COMM'
* Comparative Literature -> 'COMLIT'
* Computer Science -> 'CMPSC'
* Computing (Creative Studies) -> 'CMPTG'
* Counseling, Clinical, School Psychology  -> 'CNCSP'
* Dance -> 'DANCE'
* Dynamical Neuroscience -> 'DYNS'
* Earth Science -> 'EARTH'
* East Asian Cultural Studies -> 'EACS'
* Ecology, Evolution & Marine Biology -> 'EEMB'
* Economics -> 'ECON'
* Education -> 'EDU'
* Electrical Computer Engineering -> 'ECE'
* Engineering Sciences -> 'ENGR'
* English -> 'ENGL'
* Environmental Science & Management -> 'ESM'
* Environmental Studies -> 'ENVST'
* Excercise & Sport Studies -> 'ESS'
* Excercise Sport -> 'ES'
* Feminist Studies -> 'FEMST'
* Film and Media Studies -> 'FAMST'
* French -> 'FRENCH'
* General Studies (Creative Studies) -> 'GENST'
* Geography -> 'GEOG'
* German -> 'GER'
* Global Peace and Security -> 'GPS'
* Global Studies -> 'GLOBL'
* Graduate Division -> 'GRAD'
* Greek -> 'GREEK'
* Hebrew -> 'HEB'
* History -> 'HIST'
* Interdisciplanary -> 'INT'
* Italian -> 'ITAL'
* Japanese -> 'JAPAN'
* Korean -> 'KOR'
* Latin -> 'LATIN'
* Latin American and Iberian Studies -> 'LATST'
* Linguistics -> 'LING'
* Literature (Creative Studies) -> 'LIT'
* Marine Science -> 'MARSC'
* Materials -> 'MATRL'
* Mathematics -> 'MATH'
* Mechanical Engineering -> 'MENG'
* Media Arts and Technology -> 'MAT'
* Medieval Studies -> 'MST'
* Middle East Studies -> 'MEST'
* Militairy Science -> 'MS'
* Molecular, Cellular & Develop. Biology -> 'MCDB'
* Music -> 'MUS'
* Music and Performance Laboratories -> 'MPL'
* Philosophy -> 'PHIL'
* Physics -> 'PHYS'
* Political Science -> 'POLS'
* Portuguese -> 'PORTU'
* Psychology -> 'PSY'
* Religious Studies -> 'RST'
* Renaissance -> 'RENST'
* Slavic -> 'SLAV'
* Sociology -> 'SOC'
* Spanish -> 'SPAN'
* Speech Hearing Sciences -> 'SHS'
* Statistics & Applied Probability -> 'PSTAT'
* Technology Management -> 'TMP'
* Theater -> 'THTR'
* Writing -> 'WRIT'
* Writing & Literature (Creative Studies) -> 'WL'


