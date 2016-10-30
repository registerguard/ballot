from ballot.management.commands.ballot_settings import SITE_ADDR,\
    CSV_DIRECTORY, CSV_FILE_NAME, SCP_STRING
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

    def click_county_download(self, location):
        self.find_element_by_xpath(location).click()


class Command(BaseCommand):
    help = '''Run this one-time only per election. It DELETES all the Contest,
 Cand_yes_no and Contest model data from the previous election (It leaves the
 Region data alone, however!). It does a quick-and-dirty creation of the races
 and measures for you.'''

    def handle(self, *args, **options):
        # Check to see if there's already a copy of the .csv file downloaded
        # and delete it, if so. (OS X will auto-increment file name, won't
        # overwrite it, and we don't want that.)
        if CSV_FILE_NAME in os.listdir(CSV_DIRECTORY):
            os.remove('{0}{1}'.format(CSV_DIRECTORY, CSV_FILE_NAME))

        # Selenium replicates browser click to download .csv
        browser = ScrapingBrowser(SITE_ADDR)
        time.sleep(3)
        browser.click_county_download('/html/body/form/div[4]/div[4]/div[3]/div/div[20]/a')
        time.sleep(10)
        browser.close()
        browser.quit()

        os.system('scp {0}{1} {2}'.format(CSV_DIRECTORY, CSV_FILE_NAME, SCP_STRING))
