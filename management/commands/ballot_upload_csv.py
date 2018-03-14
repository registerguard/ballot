from ballot.management.commands.ballot_settings import SITE_ADDR,\
    CSV_DIRECTORY, CSV_FILE_NAMES, SCP_STRING
from django.core.management.base import BaseCommand, CommandError

import os
import sys
import time

try:
    from selenium import webdriver
except ImportError:
    sys.exit('This script meant for local use only.')

class ScrapingBrowser(webdriver.Chrome):
    def __init__(self, addr, *args, **kwargs):
        super(ScrapingBrowser, self).__init__(*args, **kwargs)
        self.implicitly_wait(3)
        self.get(addr)

    def click_sos_download(self, location):
        self.find_element_by_xpath(location).click()


class Command(BaseCommand):
    help = '''Simulates a browser JavaScript click required to download .csv
 file from Oregon Secretary of State website. It then uploads file to desired
 server.

 REQUIRES:
 * selenium ("pip install selenium"; it's alson listed in requirements.txt)
 * chromedriver ("https://sites.google.com/a/chromium.org/chromedriver/downloads")
     on Mac OS X, /usr/local/bin seens a good location for it)
 * working scp connection to target server'''

    def handle(self, *args, **options):
        # Selenium replicates browser click to download .csv
        browser = ScrapingBrowser(SITE_ADDR)
        time.sleep(.5)

        for csv_file_name in CSV_FILE_NAMES:
            # Check to see if there's already a copy of the .csv file downloaded
            # and delete it, if so. (OS X will auto-increment file name, won't
            # overwrite it, and we don't want that.)
            if csv_file_name['file'] in os.listdir(CSV_DIRECTORY):
                os.remove('{0}{1}'.format(CSV_DIRECTORY, csv_file_name['file']))

            browser.click_sos_download(csv_file_name['xpath'])
            time.sleep(3)

            os.system('scp {0}{1} {2}'.format(CSV_DIRECTORY, csv_file_name['file'], SCP_STRING))

        browser.close()
        browser.quit()
