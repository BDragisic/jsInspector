import json
import csv
import argparse
import time

from termcolor import colored
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_libs():
    '''
    Read the version commands from CSV file and add them to array which is interpolated into 
    a Javascript function which executes them and returns an array in the console
    '''
    array = []
    with open('./libraries.csv', 'r') as infile:
        reader = infile.readlines()

    for row in reader:
        name, command = row.split(',', maxsplit=1)

        parsedCommand = '''"%s: ".concat(eval('try { %s } catch { "Not Present" }'))''' % (
            name, command.strip())
        array.append(parsedCommand)

    command = '''function results() {var results = [];
            var arr = %s;
            for (var lib in arr) {
            results.push(eval(arr[lib]));
            }
            return results;}; return results()''' % array
    return command


def parse_args():
    parser = argparse.ArgumentParser(
        prog='jsInpector',
        description='A script to detect the versions of common JS libraries present on a webpage.',
        epilog='Developed by github.com/BDragisic and github.com/Gr4y-r0se')

    parser.add_argument(
        '-t', '--target', help='Specify a single webpage to scan'
    )

    return parser.parse_args()


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


if __name__ == '__main__':

    args = parse_args()
    print(f'''
    _     _____                           _             
   (_)   |_   _|                         | |            
    _ ___  | |  _ __  ___ _ __   ___  ___| |_ ___  _ __ 
   | / __| | | | '_ \/ __| '_ \ / _ \/ __| __/ _ \| '__|
   | \__ \_| |_| | | \__ \ |_) |  __/ (__| || (_) | |   
   | |___/_____|_| |_|___/ .__/ \___|\___|\__\___/|_|   
  _/ |                   | |                            
 |__/                    |_|                            
 
Developed by github.com/BDragisic and github.com/Gr4y-r0se
          ''')

    target = args.target if 'https' in args.target else 'https://'+args.target
    print('\nTarget:', colored(f'{target}\n', 'blue'))

    output = get_version('https://'+args.target)

    for library in output:

        name = library.split(':')[0]
        version = library.split(':')[1]

        if version != ' Not Present' and version != ' undefined':
            print(f'    [*] {name}:', colored(version, 'green'))
