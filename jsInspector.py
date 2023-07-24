import requests
import json
import csv
import argparse
import time

from packaging import version
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
        reader = [i.strip() for i in infile.readlines()]

    for row in reader:
        splitRow = row.split('|')
        name, command, npmLink = splitRow[0], splitRow[1], splitRow[2]

        nameLink = name+'|'+npmLink
        parsedCommand = '''"%s: ".concat(eval('try { %s } catch { "Not Present" }'))''' % (
            nameLink, command.strip())

        array.append(parsedCommand)

    command = '''function results() {var results = [];
            var arr = %s;
            for (var lib in arr) {
            results.push(eval(arr[lib]));
            }
            return results;}; return results()''' % array
    return command
    exit()


def parse_args():
    parser = argparse.ArgumentParser(
        prog='jsInpector',
        description='A script to detect the versions of common JS libraries present on a webpage.',
        epilog='Developed by github.com/BDragisic and github.com/Gr4y-r0se')

    parser.add_argument(
        '-t', '--target', help='Specify a single webpage to scan'
    )

    parser.add_argument(
        '-f', '--file', help='Specify path to file with a list of newline separated domains'
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

    if args.target != None:
        targets = [args.target]
    elif args.file != None:
        with open(args.file, 'r') as domainsFile:
            targets = [i.strip() for i in domainsFile.readlines()]

    for target in targets:
        target = target if 'https' in target else 'https://'+target

        print('\nTarget:', colored(f'{target}\n', 'blue'))

        output = get_version(target)

        for library in output:

            # Janky splits but works for now
            nameAndLink = library.split(':')[0]
            name = nameAndLink.split('|')[0]
            npm = nameAndLink.split('|')[1]

            _version = library.split(':')[1]
            # If the package is avaiable on the NPM registry we can extract the latest version and compare
            if npm and _version != ' Not Present' and _version != ' undefined':
                latestVersion = json.loads(
                    requests.get('https://'+npm.strip()).text)['version']

                if version.parse(_version) < version.parse(latestVersion):
                    colour = 'red'
                    name = name + " OUTDATED"
                else:
                    colour = 'green'

            else:
                latestVersion = None
                colour = 'green'

            if _version != ' Not Present' and _version != ' undefined':
                print(f'    [*] {name}:')
                print(f'        [*] Version detected: ' +
                      colored(_version, colour))
                if latestVersion:
                    print(f'        [*] Latest version: ' +
                          colored(latestVersion, colour))
