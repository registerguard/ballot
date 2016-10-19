from ballot.models import Cand_yes_no
from django.core.management.base import BaseCommand, CommandError
from xlrd import open_workbook

import os
import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = open_workbook('Lane Results.xlsx')
        sheets = wb.sheets()
        for sheet in wb.sheet_names():
            contest_number = sheet.split()[-1]
            # 0859
            out_list = []
            out_list.append( wb.sheet_by_name(sheet).cell(6,0).value )
            cand_meas_names = wb.sheet_by_name(sheet).row_values(6, 2)
            # [u'Joshua Skov', u'Emily Semple', u'Write-in']
            # [u'Yes', u'No']
            for cand_meas_name in cand_meas_names:
                out_list.append(
                    (contest_number, cand_meas_name,)
                )
            pprint.pprint( out_list )
        print str(len(sheets)).format('{0} races/contests')
