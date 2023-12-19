from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
from lxml import etree
import time

def go_to_inf_page():
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    browser.get("https://www.reg.uci.edu/perl/WebSoc")
    
    selector = browser.find_elements(By.XPATH, "//select[@name='Dept']/option")
    
    for items in selector:
        if items.get_attribute("value") == 'IN4MATX':
            items.click()
            break

    
    submit_button = browser.find_element(By.XPATH, "//input[@value='Display Web Results']")
    submit_button.click()


    inf_131 = browser.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[48]/td[11]")
    count = inf_131.text

    

    browser.quit()
    return int(count)



# if __name__ == "__main__":
#     start = time.time()
#     go_to_inf_page()
#     end = time.time()
#     print(f'Time to run: {end - start}')
