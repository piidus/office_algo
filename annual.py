from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from data import call_the_data
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Open main url
main_url = 'https://pmposhan-mis.education.gov.in/mdm_production/login.aspx'
def login(sleep_time=15):
    driver.get(main_url)
    driver.maximize_window()
    
    
    login_id = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtLogin').send_keys('RAJARHAT')
    password = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys('mdm12345')
    time.sleep(sleep_time)

def enter_annual():
    driver.find_element(By.XPATH, '//*[@id="ctl00_mc_Menu1"]/ul/li[4]/a').click()  
    WebDriverWait(driver=driver, timeout=3)
    driver.find_element(By.XPATH, '//*[@id="ctl00_mc_Menu1:submenu:13"]/li[2]/a').click()
    WebDriverWait(driver=driver, timeout=3)
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnsearch').click()
    WebDriverWait(driver=driver, timeout=3)