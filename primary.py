# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time, math
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
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
    
    
    login_id = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtLogin').send_keys(os.environ.get('login_id'))
    password = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_txtPwd').send_keys(os.environ.get('pwd'))
    time.sleep(sleep_time)

    # driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnLogin').click()
    # time.sleep(3)
    # WebDriverWait.until(method=)
    # logedin_url = driver.current_url
    # print(logedin_url)
    # driver.get(logedin_url)
    
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
    # driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_ddlfin_year"]/option[2]')
    
# ctl00_ContentPlaceHolder1_Grdschool_monthly_dtl_ctl02_hlJune_monthly_entry
# ctl00_ContentPlaceHolder1_Grdschool_monthly_dtl_ctl04_hlJune_monthly_entry
    
def set_values(id, value):
    '''id = str(html id)
        value = input as wish'''
    pri_day = driver.find_element(By.ID, id)
    pri_day.clear()
    pri_day.send_keys(str(value))
def find_school(data, sch):
    
    sch_name =str(data['SCHOOL NAME'])
    
    # start_index = sch_name.find("(")  # Find the index of the opening parenthesis
    # if start_index:
    #     sch_name = sch_name[:start_index + 1]  # Extract from the character after "("
    #     print(sch_name)
    # else:
    #     pass

    time.sleep(3)
    find_sch = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name')
    # ctl00_ContentPlaceHolder1_School_Master_Search_Ctrl_txtschool_name
    find_sch.clear()
    WebDriverWait(driver=driver, timeout=3)

    find_sch.send_keys(sch_name)
    time.sleep(1)
    # search button
    driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_btnsearch').click()
    time.sleep(3)
    # Store the ID of the original window
    original_window = driver.current_window_handle
    # click on month
    try:
        # driver.find_element(By.LINK_TEXT, 'Pending').click()
        driver.find_element(By.LINK_TEXT, 'Draft').click()
        
    except :
        # new_tab = driver.find_element(By.LINK_TEXT, 'Draft').click()
        driver.find_element(By.LINK_TEXT, 'Pending').click()
    finally:
        # time.sleep(3)
        # Wait for the new window or tab
        WebDriverWait(driver=driver, timeout=3).until(EC.number_of_windows_to_be(2))
        new_handle = driver.window_handles[-1]
        # time.sleep(3)
        driver.switch_to.window(new_handle) # Move to new Tab
        # time.sleep(1)
        total_enr = driver.find_element(By.ID, 'lblenrollment1').text.split(',')
        pp = int(total_enr[0].split('[')[1])
        pri = int(total_enr[1])
        
       
        driver.find_element(By.ID,'txtenrolbv' ).send_keys(pp)
        # set_values('txtenrolbv', data['PP ENR']) # Bal vatika enrollment
        # WebDriverWait(driver=driver, timeout=5)
        driver.find_element(By.ID, 'txtenrolpri').send_keys(pri)
        # set_values('txtenrolpri', data['PRI ENR']) #Pri Enrollment
        # time.sleep(1)
        if data['DAYS'] >= (data['PP MEAL']/pp):
            pp_days = data['DAYS']
        else:
            pp_days = math.ceil(data['PP MEAL']/pp)
        # primary days
        if data['DAYS'] >= ((data['PRI MEAL']+data['V MEAL'])/pri):
            pri_days = data['DAYS']
        else:
            pri_days = math.ceil((data['PRI MEAL']+data['V MEAL'])/pri)
        
        # DAYS
        set_values('txtbvnodays', pp_days ) # pp days
        set_values('txtpnodays', pri_days) # PRI DAYS
        set_values('txtbvactdays', pp_days) # PP SERVER DAYS
        set_values('txtpactdays', pri_days)  #Actual Days pri
        # # meal
        set_values('txtbvtotalmeal', data['PP MEAL']) # meal pp
        set_values('txtptotalmeal',  (data['PRI MEAL']+data['V MEAL']))  # pri Meal
        # Expenditure
        # expen = float(data['EXPENDITURE']) #Total Expenditure
        # pp_expen = round(data['PP'] * 5.45,2) #Calculate per student expenditure
        # pri_enpen = round(expen - pp_expen,2)
        try:
            set_values('txtcc_rec_bv', data['PP_ALLOT']) #pp receive
            set_values('txtcc_exp_bv', data['EXPEN PP']) #pp expenditure
            set_values('txtcc_rec_p', "{:.2f}".format(data['I_IV ALLOT']+data['V ALLOT']))
            time.sleep(1)
            set_values('txtcc_exp_p', "{:.2f}".format(data['EXPEN PRI']+data['EXPEN V'])) #i-v expenditure
            time.sleep(1)
        except Exception as e: 
            print('expenditure :', e)
        # set_values('txtcc_exp_p', data['']) #Allot
        # set_values('txtcc_exp_p', data['EXP TOTAL CONV TOTAL']) # Ecpenditure
        
        # total_enroll = int(data['ENROLL'])
        # if total_enroll<=25:
        #     set_values('txtcch_rec', 1500)
        # elif total_enroll>25:
        #     cch = 1500+(int(total_enroll/100)*1500)
        try:
            # cch_value = int(data['CCH COUNT']) * 1500
            # # driver.find_element(By.ID, 'txtcch_rec' ).send_keys(cch_value)
            cch = int(driver.find_element(By.ID, 'lblcch_exp').get_attribute('value'))
            set_values('txtcch_rec', cch)
            # print(int(data['CCH COUNT'])*1500)
            # set_values('txttexp', data['MME'])
        except Exception as e:
            print('cch', e)
        # # rICE
        # Calculate rice by total expenditure
        # total_rice_expense = int(data['RICE EXPEN'])
        # if total_rice_expense > 1:
        #     pp_rice_allot = data['PP_R_ALLOT']
        #     pp_rice_expen = round(data['PP MEAL']*0.10,2)
            
        #     pri_rice_allot = data['I-V_R_ALLOT']
        #     pri_rice_expen = round(total_rice_expense - pp_rice_expen,2)
        # else:
        #     pp_rice_allot = 0
        #     pp_rice_expen = round(data['PP MEAL']*0.10,2)
        #     pri_rice_allot = 0
        #     pri_rice_expen = round(total_rice_expense - pp_rice_expen,2)
        

        try:
            set_values('grd_food_BV_ctl03_txtrec', data['PP_R_ALLOT']) #pp rice 
            time.sleep(1)
            set_values('grd_food_BV_ctl03_txtConsumption', data['PP-RICE-EXPEN']) #pp rice expen
            time.sleep(1)
            set_values('grd_food_Primary_ctl03_txtrec', "{:.2f}".format(data['I-IV_R_ALLOT'] +  data['V_R_ALLOT']))
            time.sleep(1)
            set_values('grd_food_Primary_ctl03_txtConsumption', "{:.2f}".format(data['PRI-RICE-EXPEN'] + data['V -RICE-EXPEN']))
            time.sleep(1)
        except Exception as e:
            print('Rice :', e)

        # iNSPECTION
        # driver.find_element(By.ID, 'rdSchoolInspection_0').click()
        # set_values(id='txtinsp3', value=1)
        
        # driver.find_element(By.ID, 'btnsavedrft').click() # save as draft
        driver.find_element(By.ID, 'btnfreeze').click()  #Freeze 
        
        alert = WebDriverWait(driver=driver, timeout=3).until(EC.alert_is_present())
        
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        
        # time.sleep(300)
        
        driver.switch_to.window(original_window)    # #Switch back to the old tab or window
        print('School entry complete ::: ', sch_name)
        time.sleep(3)
        #Close the tab or window
        # driver.close()
# call the functions
login()
monthly_data()
data = call_the_data(3)
# one_time = 1
for index, row in data.iterrows():
    try:
        print(row['SCHOOL NAME'])
        
        sch = data['SCHOOL NAME']
        find_school(row, sch)
        
    except Exception as e:
            print(e)

# time.sleep(15)
print(data)