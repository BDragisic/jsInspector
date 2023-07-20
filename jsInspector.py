import argparse
import time

from termcolor import colored
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 2D array of common JS packages and the console commands to reveal their version
libraries = [
    # ["Adobe Target", "adobe.target.VERSION", ''],
    # ["Angular", "getAllAngularRootElements()[0].attributes['ng-version']",
    #  'https://code.angularjs.org/'],
    # ["AngularJS", "angular.version.full", 'https://code.angularjs.org/'],
    # ["Bootstrap", "bootstrap.Alert.VERSION ",
    #     'https://getbootstrap.com/docs/versions/'],
    # ["Bootstrap", "$.fn.tooltip.Constructor.VERSION",
    #     'https://getbootstrap.com/docs/versions/'],
    ["Core", "core.version", 'https://www.npmjs.com/package/core-js'],
    ["Core", "window['__core-js_shared__'].versions[0].version",
        'https://www.npmjs.com/package/core-js'],
    ["D3", "d3.version", 'https://github.com/d3/d3/releases'],
    ["Data Tables", "$.fn.dataTable.version",
        'https://cdn.datatables.net/releases.html'],
    ["Data Tables", "$().dataTable.version",
     'https://cdn.datatables.net/releases.html'],
    ["Dojo", "dojo.version", 'https://github.com/dojo/dojo'],
    ["Dropzone", "Dropzone.version", 'https://www.npmjs.com/package/dropzone'],
    ["Ember.js", "Ember.VERSION", 'https://emberjs.com/releases/'],
    ["ExtJS 3.x", "Ext.version", 'https://www.sencha.com/products/extjs/'],
    ["ExtJS 4.0", "Ext.getVersion('extjs')",
     'https://www.sencha.com/products/extjs/'],
    ["ExtJS >= 4.1", "Ext.getVersion().version",
     'https://www.sencha.com/products/extjs/'],
    ["FancyBox", "jQuery.fancybox.version", 'http://fancybox.net/'],
    ["Highcharts", "Highcharts.version",
        'https://www.npmjs.com/package/highcharts?activeTab=versions'],
    ["jQuery", "jQuery().jquery", 'https://releases.jquery.com/jquery/'],
    ["jQueryUI", "jQuery.ui.version", 'https://releases.jquery.com/ui/'],
    ['jQueryUI', "$.ui.version", 'https://releases.jquery.com/ui/'],
    ["Knockout.js", "ko.version", 'https://knockoutjs.com/downloads/'],
    ["Lodash", "_.VERSION", 'https://www.npmjs.com/package/lodash?activeTab=versions'],
    ["Microsoft Clarity", "clarity.v", 'https://www.npmjs.com/package/clarity-js'],
    ["Migrate", "jQuery.migrateVersion", 'https://releases.jquery.com/jquery/'],
    ["Modernizr", "Modernizr._version", 'https://www.npmjs.com/package/modernizr'],
    ["Moment", "moment.version", 'https://www.npmjs.com/package/moment'],
    ["Prototype", "prototype.version", 'http://prototypejs.org/download/'],
    ["React", "React.version", 'https://github.com/facebook/react/releases'],
    ["RequireJS", "require.version", 'https://requirejs.org/docs/download.html'],
    ["Toastr", "toastr.version", 'https://www.npmjs.com/package/toastr'],
    ["Wordpress Emoji", "window._wpemojiSettings.source.concatemoji",
        'https://wordpress.org/support/topic/wp-emoji-release-min-js/'],
    ["YUI", "Y.VERSION", 'https://clarle.github.io/yui3/']
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
        print(
            f'    [*] Checking {package[0]}                                       ', end='\r')
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
            print(f'\n    [*] {package[0]}:')
            print('        [*] Version detected:',
                  colored(versionDetected, 'green'))
            print('        [*] Latest release:',
                  colored(package[2], 'green'))
