#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_cell_magic('capture', '', '!pip install selenium')


# In[1]:


get_ipython().run_cell_magic('capture', '', '!wget https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_linux64.zip')


# In[8]:


get_ipython().system('unzip chromedriver_linux64.zip')


# In[10]:


get_ipython().system('pip install pyserial')


# In[21]:


from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import serial
import time
from IPython.display import Image


# Read in the configuration file for OLX account credentials and chrome path.

# In[ ]:


# Read in the credentials for olx account and chrome
read_config = configparser.ConfigParser()
read_config.read("credentials.ini")

phone = int(read_config.get("OLX", "phone"))
password = str(read_config.get("OLX", "pass"))
chrome_path = str(read_config.get("CHROME", "path"))


# We can log-in to the OLX account using either phone or gmail or user and password. Trying to log-in via gmail causes the following issue for which I couldn't find a workaround:

# In[23]:


Image(url='couldntSignIn.png', width=500)


# Thus, I tried logging in via phone instead, and it worked just fine!

# In[20]:


cap = DesiredCapabilities.CHROME
cap['chrome.switches'] = ['--disable-local-storage']
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir="+chrome_path)
options.add_argument("--disable-extensions")
options.add_argument("--incognito");
options.add_argument("--set-headless")
chrome_driver =os.getcwd() + '/chromedriver'
os.environ["webdriver.chrome.driver"] = chrome_driver

while(True):
    with serial.Serial('/dev/ttyACM0', 9800, timeout=1) as ser:
        try:
            driver = webdriver.Chrome(executable_path=chrome_driver,options=options, desired_capabilities=cap)
            #Now go to olx page, click on login
            driver.get("https://www.olx.in/")
            #Login:
            login_button = driver.find_element_by_xpath("//button[.//span[text()='Login']]")
            login_button.click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH,"//button[.//span[text()='Continue with Phone']]")))

            driver.find_element_by_xpath("//button[.//span[text()='Continue with Phone']]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.NAME,'phone')))

            driver.find_element_by_name('phone').send_keys(phone)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath("//button[.//span[text()='Next']]").click()
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.NAME,'password')))

            driver.find_element_by_name('password').send_keys(password)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('//button[.//span[text()="Log in"]]').click()
            wait.until(EC.presence_of_element_located((By.XPATH,"//div[@data-aut-id='iconProfile']")))


            #Now we are logged in!
            driver.get('https://www.olx.in/nf/chat')
            wait.until(EC.presence_of_element_located((By.XPATH,"//span[.//span[text()='Inbox']]")))
            unread_count_tag = driver.find_elements_by_xpath("//span[.//span[text()='Inbox']]/following-sibling::div/span")
            if(len(unread_count_tag) == 0):
                print(f'You have no new messages!')
                ser.write(b'L')
                time.sleep(1)
            else:
                print(f'You have {unread_count_tag[0].text} new messages!')
                ser.write(b'H')
                time.sleep(1)

        except Exception as e:
            print(e)
        finally:
            driver.close()


# **Next Steps**:
# 1. Notify me if there are any unread messages using notification/arduino LED.
# 2. Implement the same using image processing to see if that's faster.
