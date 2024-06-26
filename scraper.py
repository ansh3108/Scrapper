from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, re, os,time


download_folder = "ENTER_PATH_HERE"


artists = ["drakeofficial","joji"]

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_experimental_option("prefs", {
"download.default_directory": download_folder,
"download.prompt_for_download": False,
"download.directory_upgrade": True,
"safebrowsing.enabled": True
})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

music_id = {}
for artist_id in artists:
    artist_id = artist_id.strip().lower()
    url = f"https://www.youtube.com/@{artist_id}/videos"
    driver.get(url)
    wait.until(EC.visibility_of_element_located((By.ID, 'text-container')))
    time.sleep(random.randint(0,6))
    video_title = driver.find_elements(By.ID,"video-title-link")
    music_id[artist_id] = []
    for tag in video_title:
        youtube_url = tag.get_attribute("href")
        pattern = r"(?<=v=)[a-zA-Z0-9_-]+"
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(0)
            music_id[artist_id].append(video_id)
    time.sleep(random.randint(2,7))

for artists in music_id:
    for music in music_id[artists]:
        download_url = f"https://y2mate.nu/"
        video_url = f"https://www.youtube.com/watch?v={music}"
        driver.get(download_url)
        wait.until(EC.visibility_of_element_located((By.ID, 'url')))
        time.sleep(2)
        driver.find_element(By.ID, 'url').send_keys(video_url)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,"body > form > div:nth-child(2) > input[type=submit]:nth-child(2)").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > form > div:nth-child(2) > a:nth-child(1)')))
        time.sleep(2)
        download_link = driver.find_element(By.CSS_SELECTOR, 'body > form > div:nth-child(2) > a:nth-child(1)').get_attribute('href')
        initial_count = len([f for f in os.listdir(download_folder) if f.endswith(".mp3")])
        file_downloaded = False
        driver.get(download_link)
        while not file_downloaded:
            time.sleep(1)
            current_count = len([f for f in os.listdir(download_folder) if f.endswith(".mp3")])
            if current_count > initial_count:
                file_downloaded = True
        time.sleep(random.randint(2,10))
        random_number = random.randint(0,9999)
        if random_number%3==0:
            driver.delete_all_cookies()
    time.sleep(1)
    

time.sleep(60)

driver.quit()
