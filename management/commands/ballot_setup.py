from ballot.models import Cand_yes_no
from django.core.management.base import BaseCommand, CommandError

import os
import sys
import time

try:
    from selenium import webdriver
except ImportError:
    sys.exit('This script meant for local use only.')

SITE_ADDR = 'http://results.oregonvotes.gov/ResultsExport.aspx'
BROWSER_DOWNLOAD_DIR = '/Users/jheasly/Downloads'
CSV_FILE_NAME = 'Lane_County_Media_Export.csv'

class ScrapingBrowser(webdriver.Chrome):
    def __init__(self, addr, *args, **kwargs):
        super(ScrapingBrowser, self).__init__(*args, **kwargs)
        self.implicitly_wait(3)
        self.get(addr)

    def click_county_download(self, location):
        self.find_element_by_xpath(location).click()


class Command(BaseCommand):
    # TODO: Prior to download, check to see if there's already and
    # Lane_County_Media_Export.csv and if so, DELETE ...

    help = '''Run this one-time only per election. It DELETES all the Contest,
 Cand_yes_no and Contest model data from the previous election (It leaves the
  Region data alone, however!). It does a quick-and-dirty creation of the races
  and measures for you.'''

    def handle(self, *args, **options):
        # Selenium replicates browser click to download .csv
        browser = ScrapingBrowser(SITE_ADDR)
        time.sleep(3)
        browser.click_county_download('/html/body/form/div[4]/div[4]/div[3]/div/div[20]/a')
        time.sleep(10)
        browser.close()
        browser.quit()

        # e.g., /Users/jheasly/Development/ballot/management
        FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


        # '''
        # START Excel sheets
        # '''
        # wb = open_workbook('Lane Results.xlsx')
        # sheets = wb.sheets()
        # for sheet in wb.sheet_names():
        #     contest_number = sheet.split()[-1]
        #     # 0859
        #     out_list = []
        #     out_list.append( wb.sheet_by_name(sheet).cell(6,0).value )
        #     cand_meas_names = wb.sheet_by_name(sheet).row_values(6, 2)
        #     # [u'Joshua Skov', u'Emily Semple', u'Write-in']
        #     # [u'Yes', u'No']
        #     for cand_meas_name in cand_meas_names:
        #         out_list.append(
        #             (contest_number, cand_meas_name,)
        #         )
        #     pprint.pprint( out_list )
        # print str(len(sheets)).format('{0} races/contests')
        # '''
        # END Excel sheets
        # '''
