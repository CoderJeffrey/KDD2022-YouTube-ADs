from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
from selenium.webdriver.support.ui import WebDriverWait

videos = set()
#visited video ads (to filter out duplicated video ads)
visited = set()

with open("EXAMPLE_videoid.txt","r") as f:
    lines = f.readlines()
for line in lines:
    videos.add(line.strip())
f.close()
prev = ""

#store the result in v_RESULT.txt (change to any other name you prefer)
output = open("v_RESULT.txt","w", encoding="utf-8")

for l in videos:
    #connect to the Youtube video page
    toget = "https://www.youtube.com/watch?v=" + l
    print("toget",toget)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--public")
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

    for i in range(1,3):
        try:
            driver.get(toget)
            driver.refresh()
            
            #get the innerHTML of the video page
            html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
            commas = str(html).split(",")

            #get the adVideo id tag
            for line in commas:            
                if('adVideoId"' in str(line)):
                    reverse = line[::-1]
                    # print(reverse + " REVERSED \n ")
                    end = reverse.find('\"')
                    start = reverse[end+1:].find('\"') + (end+1)
                    ad_video_id = str(line[-start: -end-1])

                    #if ad_video_id is unique, add them to the final output file
                    if ad_video_id not in visited:
                        output.write(ad_video_id +"\n")
                        visited.add(ad_video_id)

            #refresh the video page to extract updated meta data
            time.sleep(5)
            driver.refresh()
            driver.switch_to_window(driver.window_handles[1])
            driver.refresh()
        
        except:
            continue
    driver.close()
output.close()
