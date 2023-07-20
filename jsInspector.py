import argparse
import time

from termcolor import colored
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Common 2D array of JS packages and the console commands to reveal their version
libraries = [
    ["Adobe Target", "adobe.target.VERSION"],
    ["Angular", "getAllAngularRootElements()[0].attributes['ng-version']"],
    ["AngularJS", "angular.version.full"],
    ["Bootstrap", "bootstrap.Alert.VERSION "],
    ["Bootstrap", "$.fn.tooltip.Constructor.VERSION"],
    ["Core", "core.version"],
    ["Core", "window['__core-js_shared__'].versions[0].version"],
    ["D3", "d3.version"],
    ["Data Tables", "$.fn.dataTable.version"],
    ["Data Tables", "$().dataTable.version"],
    ["Dojo", "dojo.version"],
    ["Dropzone", "Dropzone.version"],
    ["Ember.js", "Ember.VERSION"],
    ["ExtJS 3.x", "Ext.version"],
    ["ExtJS 4.0", "Ext.getVersion('extjs')"],
    ["ExtJS >= 4.1", "Ext.getVersion().version"],
    ["FancyBox", "jQuery.fancybox.version"],
    ["Highcharts", "Highcharts.version"],
    ["jQuery", "jQuery().jquery"],
    ["jQueryUI", "jQuery.ui.version"],
    ['jQueryUI', "$.ui.version"],
    ["Knockout.js", "ko.version"],
    ["Lodash", "_.VERSION"],
    ["Microsoft Clarity", "clarity.v"],
    ["Migrate", "jQuery.migrateVersion"],
    ["Modernizr", "Modernizr._version"],
    ["Moment", "moment.version"],
    ["Prototype", "prototype.version"],
    ["React", "React.version"],
    ["RequireJS", "require.version"],
    ["Toastr", "toastr.version"],
    ["Wordpress Emoji", "window._wpemojiSettings.source.concatemoji"],
    ["YUI", "Y.VERSION"]
]


def parse_args():
    parser = argparse.ArgumentParser(
        prog='jsInpector',
        description='A script to detect the versions of common JS libraries present on a webpage.',
        epilog='Developed by github.com/BDragisic')

    parser.add_argument(
        '-t', '--target', help='Specify a single webpage to scan'
    )

    return parser.parse_args()


def get_version(url, query):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = webdriver.Chrome(options=options, service=chrome_service)
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(5)

    # Use built in Selenium method to execute the console commands.
    driver.get(url)
    version = driver.execute_script(f'return {query}')
    time.sleep(0.1)
    driver.quit()
    return version


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
 
Developed by github.com/BDragisic
          ''')

    target = args.target if 'https' in args.target else 'https://'+args.target
    print('\nTarget:', colored(f'{target}\n', 'blue'))
    for package in libraries:
        command = package[1]
        try:
            versionDetected = get_version(target, command)
        except KeyboardInterrupt:
            break
        except:
            # If console commands returns error, presumably the JS package doesn't exist
            continue

        if versionDetected:
            # driver.execute_script() returns None if the commands returned nothing
            print(f'    [*] {package[0]}:',
                  colored(f'{versionDetected}', 'green'))
