from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time

from .libraries import get_libs


def get_version(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = webdriver.Chrome(options=options, service=chrome_service)
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(5)

    # Use built in Selenium method to execute the console commands.
    driver.get(url)

    script = get_libs()
    versions = driver.execute_script(script)
    time.sleep(0.1)
    driver.quit()
    return versions
