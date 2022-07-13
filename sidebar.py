from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.support.ui import WebDriverWait

import json

#extract videos from a file
videos = set()

#change to the file with video name
with open("EXAMPLE_sidebarid.txt", "r") as f:
    lines = f.readlines()
for p in lines:
    videos.add(p.strip())
f.close()

prev = ""
info = []

fname = "s_RESULT.txt"
output = open(fname, "w", encoding="utf-8")

for l in videos:
    #connect to the youtube video page
    toget = "https://www.youtube.com/watch?v=" + l
    print("toget",toget)


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--public")
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

    for i in range(1,2):
        try:
            driver.get(toget)
            #get the innerHTML of the video page
            html = driver.execute_script("return document.getElementsByTagName('html')[0 ].innerHTML")

            all_info = str(html)
            #return the extracted metadata to S_RESULT.txt (change s_RESULT.txt to any output file you prefer)

            if "promotedSparklesWebRenderer" in all_info:
                place = all_info.find("promotedSparklesWebRenderer")
                info = all_info[place:place+2000]

                #extract the title tag
                if "title" in info:
                    title_place = info.find("title")
                    end_place = info[title_place:].find("}")
                    line_sub_title = info[title_place+22:title_place+end_place-1]

                #extract the description tag
                if "description" in info:
                    title_place = info.find("description")
                    end_place = info[title_place:].find("}")
                    line_sub_description = info[title_place+28:title_place+end_place-1]

                #extract the website URL
                if "websiteText" in info:
                    title_place = info.find("websiteText")
                    end_place = info[title_place:].find("}")
                    line_sub_website = info[title_place+28:title_place+end_place-1]
                if l:
                    output.write(f"{l} | ")
                    output.write(f"{line_sub_title} | ")
                    output.write(f"{line_sub_description} | ")
                    output.write(f"{line_sub_website} \n")
                time.sleep(5)    
            """
            output the content is the following format
            video id | title | description | website url  
            """
        
        except:
            continue
    driver.close() 
output.close()
