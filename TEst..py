import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get(url='https://pmposhan-mis.education.gov.in/mdm_production/login.aspx')
time.sleep(3)
driver.quit()