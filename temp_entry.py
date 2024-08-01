from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from temp_data import call_the_data 
import time, os

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

main_url = 'https://pmposhan-mis.education.gov.in/mdm_production/login.aspx'

def login(sleep_time=15):
    driver.get(main_url)
    driver.maximize_window()
    
    
    login_id = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtLogin').send_keys(os.environ.get('login_id'))
    password = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(os.environ.get('pwd'))
    time.sleep(sleep_time)

def set_values(id, value):
    '''id = str(html id)
        value = input as wish'''
    pri_day = driver.find_element(By.ID, id)
    pri_day.clear()
    alert = WebDriverWait(driver=driver, timeout=3).until(EC.alert_is_present())
            
    alert = driver.switch_to.alert
    alert.accept()
    pri_day.send_keys(str(value))
def monthly_data():
    # Create an object of the Select class
    driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[1]/ul/li[4]/a').click()
    
    WebDriverWait(driver=driver, timeout=3)
    # driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[1]/ul/li[4]/ul/li[1]/a').click()
    driver.find_element(By.XPATH, '//*[@id="ctl00_mc_Menu1:submenu:13"]/li[2]/a').click()
    
    WebDriverWait(driver=driver, timeout=3)
    # find year
    driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_ddlfin_year"]/option[2]').click() #2024-25
    # driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_ddlfin_year"]/option[3]').click() #2023-24
    WebDriverWait(driver=driver, timeout=3)


def find_school(data, sch):
    
    sch_name =str(data['Name of the Institution']).split('(')[0]
    
    

    time.sleep(3)
    find_sch = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name')
    # ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name
    find_sch.clear()
    WebDriverWait(driver=driver, timeout=3)

    find_sch.send_keys(sch_name)
    time.sleep(1)
    
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # click on month
    # IN FOR LOOP FIND DRAFT TO SAVE
    
    for _ in range(3):
        # search button
        driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnsearch').click()
        time.sleep(3)
        find_school =driver.find_element(By.LINK_TEXT, 'Draft')
        time.sleep(1)
        if find_school:
            find_school.click()
    

            WebDriverWait(driver=driver, timeout=3).until(EC.number_of_windows_to_be(2))
            new_handle = driver.window_handles[-1]
            driver.switch_to.window(new_handle)
            # SAVE ENROLLMENT
            total_enr = driver.find_element(By.ID, 'lblenrollment1').text.split(',')
            print('total_enr -------------------', total_enr)
            pp = int(total_enr[0].split('[')[1])
            pri = int(total_enr[1])
            up = int(total_enr[2].split(']')[0])
            print('total_enr -------------------', pp, pri)
            # set enrollment
            # driver.find_element(By.ID,'txtenrolbv' ).send_keys(pp)
            try:
                # ppbos =driver.find_element(By.ID,'txtenrolbv' )
                # ppbos.clear()
                # ppbos.send_keys(pp)
                set_values('txtenrolbv', pp)
                set_values('txtenrolpri', pri)
                set_values('txtenrolupri', up)
            except Exception as e:
                print(e)
            # driver.find_element(By.ID, 'txtenrolpri').send_keys(pri)
            # time.sleep(20)

            time.sleep(3)
            driver.find_element(By.ID, 'btnfreeze').click()  #Freeze 
            
            alert = WebDriverWait(driver=driver, timeout=3).until(EC.alert_is_present())
            
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(1)
            
            # time.sleep(300)
            
            driver.switch_to.window(original_window)    # #Switch back to the old tab or window
            print('School entry complete ::: ', sch_name, )
            time.sleep(3)
        else:
            break

if __name__ == '__main__':
    #  call the functions
    login()
    monthly_data()
    data = call_the_data(89)
    # one_time = 1
    for index, row in data.iterrows():
        try:
            print(row['Name of the Institution'])
            
            sch = data['Name of the Institution']
            find_school(row, sch)
            
        except Exception as e:
                print(e)

    # time.sleep(15)
    print(data)