from ballot.models import Cand_yes_no
from django.core.management.base import BaseCommand, CommandError
from xlrd import open_workbook
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = open_workbook('Lane Results.orig.xlsx')
        sheets = wb.sheets()
        for sheet in sheets:
            print sheet.name
        print str(len(sheets)).format('{0} races/contests')
