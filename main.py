from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

links = []
covers = []
titles = []
external = []

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


service = Service(executable_path='chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://ww2.123moviesfree.net/search/?q=breaking+bad")

element=driver.find_elements(By.XPATH, "/html/body/main/div/div[@class='card-body p-0']/div[@id='resdata']/div[@class='col']/div[@class='card h-100 border-0 shadow']/a") # using XPATH to find link to movie

for col in element:
    data = col.get_attribute("outerHTML").split("<") #spliting data into seperate parts to be easier read
    links.append("https://ww2.123moviesfree.net"+data[1].strip('a href="').strip('" class="rounded poster">')) # removing other parts of html to leave only the link to the movie
    covers.append(data[2][data[2].find('data-src='):].strip('" class="lazy card-img-top entered loaded" data-ll-status="loaded">').strip('data-src="') + "pg") # I have no clue why but i neeeeeed to add the + pg at the end of this because for some reason when I am splicing off the other parts of the HTML it gets rid of it
    titles.append(data[4].replace('h2 class="card-title text-light fs-6 m-0">',''))

for link in links: # do following for all of the movies or tv shows
    driver.get(link)
    #getting episode list to find if movie or tv show
    element = driver.find_elements(By.XPATH,"/html/body/main/div/div/div[@class='card border-0 mb-3 shadow']/div/div/div[@class='col-md-3']/div/div[@id='eps-list']")
    for v in element:
        #get children of parrent to find # of episodes
        childrens = v.find_elements(By.XPATH,"./child::*")
        match childrens[0].get_attribute("id"):
            case 'ep-1': #if child is equal to ep-1 we know that there is only 1 episode and therefore a movie
                l = driver.find_element(By.ID, "play-now")
                driver.execute_script("arguments[0].click();", l) #click button so video is loaded and we can scrape it
                src = ui.WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH,"/html/body/main/div/div/div[@class='card border-0 mb-3 shadow']/div/div/div/div/iframe").get_attribute("src"))  # waiting for link to load in order to scrape the link
                external.append(src) # append link to list titled external
            case _ :
                pass # this is for if it is a series
print(titles)
print(external)
driver.quit()