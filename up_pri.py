from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from data import call_the_data

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
# Open main url
main_url = 'https://pmposhan-mis.education.gov.in/mdm_production/login.aspx'

def login(sleep_time=15):
    driver.get(main_url)
    driver.maximize_window()
    
    
    login_id = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtLogin').send_keys('RAJARHAT')
    password = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys('mdm12345')
    time.sleep(sleep_time)

    
    
def monthly_data():
    # Create an object of the Select class
    driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[1]/ul/li[4]/a').click()
    
    WebDriverWait(driver=driver, timeout=3)
    driver.find_element(By.XPATH, '/html/body/form/div[4]/div/div[1]/ul/li[4]/ul/li[3]/a').click()
    WebDriverWait(driver=driver, timeout=3)
    # find year
    driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_ddlfin_year"]/option[2]').click()
    
    
def set_values(id, value):
    '''id = str(html id)
        value = input as wish'''
    pri_day = driver.find_element(By.ID, id)
    pri_day.clear()
    pri_day.send_keys(str(value))

def find_school(data, sch):
    
    
    time.sleep(3)
    find_sch = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name')
    # ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name
    find_sch.clear() # Clear the search box
    WebDriverWait(driver=driver, timeout=3)

    find_sch.send_keys(data['NAME TRGMDM']) # set school name
    # search button
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnsearch').click()
    time.sleep(3)
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # click on month
    try:
        driver.find_element(By.LINK_TEXT, 'Pending').click()
        # driver.find_element(By.LINK_TEXT, 'Draft').click()
        
    except :
        new_tab = driver.find_element(By.LINK_TEXT, 'Draft').click()
    finally:
        # Wait for the new window or tab
        WebDriverWait(driver=driver, timeout=3).until(EC.number_of_windows_to_be(2))
        new_handle = driver.window_handles[-1]
        time.sleep(3)
        driver.switch_to.window(new_handle) # Move to new Tab
        time.sleep(1)
       
        
        # Enrollment section
        WebDriverWait(driver=driver, timeout=5)
        total_enr = driver.find_element(By.ID, 'lblenrollment1').text.split(',')
        pri = int(total_enr[1])
        uppri = int(total_enr[2].split(']')[0])
        # print(pri, uppri)
        driver.find_element(By.ID, 'txtenrolpri').send_keys(pri)
        # set_values('txtenrolupri', uppri)
        time.sleep(1)
        driver.find_element(By.ID,'txtenrolupri' ).send_keys(uppri)
        time.sleep(1)
        # set_values('txtenrolpri', data['PRI ENR']) #Pri Enrollment
        time.sleep(1)
        # DAYS
        if data['PRI ENR'] == 0:
            set_values('txtupnodays', data['DAYS'] ) # 
            set_values('txtupactdays', data['DAYS'])  # Up pri server days
        else:
            set_values('txtpnodays', data['DAYS']) # PRI DAYS
            set_values('txtupnodays', data['DAYS'] ) # updays
            set_values('txtpactdays', data['DAYS']) # Pri SERVER DAYS
            set_values('txtupactdays', data['DAYS'])  # Up pri server days
        # meal
        if data['PRI ENR'] == 0:
            set_values('txtuptotalmeal', data['VI-VIII']) # uppri Meal
        else:
            set_values('txtptotalmeal',  data['I-V'])  # pri Meal
            set_values('txtuptotalmeal', data['VI-VIII']) # uppri Meal
        # Expenditure
        expen = float(data['EXPENDITURE']) #Total Expenditure
        pri_stu_enpen = round(data['I-V'] * 5.45, 2)
        up_stu_expen = round(expen -pri_stu_enpen, 2) #Upper primary expenditure
        
        try:
            # set_values('txtcc_rec_p', pri_stu_enpen) #pri receive
            if data['PRI ENR'] == 0:
                set_values('txtcc_exp_up', up_stu_expen) #up expenditure
            else:            
                set_values('txtcc_exp_p', pri_stu_enpen) #pri expenditure
                set_values('txtcc_exp_up', expen-pri_stu_enpen) #up expenditure
        except Exception as e:
            print('expenditure :', e)
       
        try:
            cch_value = (data['CCH COUNT']) * 1500
            # driver.find_element(By.ID, 'txtcch_rec' ).send_keys(cch_value)
            set_values('txtcch_rec', cch_value)
            print(int(data['CCH COUNT'])*1500)
            set_values('txttexp', data['MME'])
        except Exception as e:
            print('cch', e)
        # rICE

        total_rice = int(data['RICE ALLOT'])
        if total_rice == 0:
            pri_rice_expen = round(data['I-V']*0.10, 2)
            uppri_rice_expen = round(data['RICE EXPEN']-pri_rice_expen,2)
            up_pri_rice_allot = 0
        else:
            pri_rice_expen = round(data['I-V']*0.10, 2)
            up_pri_rice_allot = total_rice - pri_rice_expen
            uppri_rice_expen = round(data['RICE EXPEN']-pri_rice_expen,2)
        try:
            if data['PRI ENR'] == 0:
                set_values('grd_food_UpperPrimary_ctl03_txtuprec', up_pri_rice_allot)
                set_values('grd_food_UpperPrimary_ctl03_txtupConsumption', uppri_rice_expen)
            else:
                set_values('grd_food_Primary_ctl03_txtrec', pri_rice_expen) #pri rice allot
                set_values('grd_food_Primary_ctl03_txtConsumption', pri_rice_expen) #pri rice expen
                set_values('grd_food_UpperPrimary_ctl03_txtuprec', up_pri_rice_allot)
                set_values('grd_food_UpperPrimary_ctl03_txtupConsumption', uppri_rice_expen)
        except Exception as e:
            print('Rice :', e)
        driver.find_element(By.ID, 'btnfreeze').click()
        WebDriverWait(driver=driver, timeout=3)
        time.sleep(3)

        alert = WebDriverWait(driver=driver, timeout=3).until(EC.alert_is_present())
        
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(5)
        #Close the tab or window
        # driver.close()
        driver.switch_to.window(original_window)
       
        time.sleep(3)
# call the functions
login()
monthly_data()
data = call_the_data(3)
# one_time = 1
for index, row in data.iterrows():
    try:
        print(row['NAME TRGMDM'])
        
        sch = data['NAME TRGMDM']
        find_school(row, sch)
        
    except Exception as e:
            print(e)

# time.sleep(15)
print(data)