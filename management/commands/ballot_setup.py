from ballot.management.commands.ballot_settings import CSV_FILE_NAMES

from ballot.models import Cand_yes_no, Contest, Contest_wrapper, Region
from django.core.management.base import BaseCommand, CommandError

import csv
import os
import sys
import time

HEADER_CUTOFF = 1
AFFILIATION_LOOKUP = {
    'CON': 'C',
    'DEM': 'D',
    'IND': 'I',
    'LBT': 'L',
#     'LIB': 'L',
#     'PCE': 'P',
    'PRO': 'P',
#     'PGN': 'PG',
    'PGP': 'PG',
    'REP': 'R',
    'WFP': 'WF',
    'NON': 'N',
}
FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__)))


class GroupBy(dict):
    def __init__(self, seq, key=lambda x:x):
        for value in seq:
            k = key(value)
            self.setdefault(k, []).append(value)
    __iter__ = dict.iteritems


class Command(BaseCommand):
    help = '''Run this one-time only per election. It DELETES all the Contest,
 Cand_yes_no and Contest model data from the previous election (It leaves the
  Region data alone, however!). It does a quick-and-dirty creation of the races
  and measures for you.'''

    def handle(self, *args, **options):
        # Flush out data from previous grab.
        Contest.objects.all().delete()
        Cand_yes_no.objects.all().delete()
        Contest_wrapper.objects.all().delete()

        for csv_file_name in CSV_FILE_NAMES:
            '''
            Here we create a heirarchical Python data structure from the flat
            .csv data for ingestion into Djano app further down ...
            '''
            csvfile = open(os.path.join(FILE_PATH, csv_file_name['file']), 'rb')
            lines = list(csv.reader(csvfile))

            header_lines = lines[0:HEADER_CUTOFF]
            for header_line in header_lines:
                print '[Header line] of {0}: {1}'.format(csv_file_name['file'], header_line)

            body_lines = lines[HEADER_CUTOFF:]
            data = []

            for line in body_lines:
                data.append((
                int(line[0]),           # 'ContestID'
                line[1].strip(),        # 'ContestName'
                line[2],                # 'PartyCode'
                int(line[7]),           # 'CandidateID'
                line[8].strip(),        # 'CandidateName'
                line[9],                # 'CurrentDateTime'
                int(line[10]),          # 'VoteFor'
                int(line[11]),          # 'CandidateVotes'
                float(line[12]),        # 'CandidatePercentage'
                line[13],               # 'PrecinctsReporting'
                ))

            out_list = []
            record_list = []
            sub_list = []
            '''
            Creates a parent list/sub-list (see examples below) grouped by whatever
            item 'r[x]' selects in the original "flat" list. The key for the parent list
            is a duplicate of whatever value r[x] is.
            '''
            for k, g in GroupBy(data, key=lambda r: r[0]): # <- this is the field you group on
                record_list.append(k)
                for record in g:
                    sub_list.append(record)
                record_list.append(sub_list)
                sub_list = []
                out_list.append(record_list)
                record_list = []

            for item in out_list:
                print item[0] # <- field grouped on
                for foo in item[1]:
                    print foo

            '''
            AS OF NOV. 2016 (AND THE NEW OR S.O.S. AS SOLE SOURCE), THE DATA STRUCTURE IS MORE LIKE THIS ...

            [300019191,
            [(300019191, 'United States President and Vice President', 'REP', 300027550, 'Donald J Trump / Mike Pence', '10/28/2016 6:53:36 PM', 1, 149, 0.0909090909090909, '837/1311')
            (300019191, 'United States President and Vice President', 'DEM', 300027862, 'Hillary Clinton / Tim Kaine', '10/28/2016 6:53:36 PM', 1, 298, 0.181818181818182, '837/1311')
            (300019191, 'United States President and Vice President', 'PGP', 300027774, 'Jill Stein / Ajamu Baraka', '10/28/2016 6:53:36 PM', 1, 447, 0.272727272727273, '837/1311')
            (300019191, 'United States President and Vice President', 'LBT', 300027773, 'Gary Johnson / Bill Weld', '10/28/2016 6:53:36 PM', 1, 596, 0.363636363636364, '837/1311')
            (300019191, 'United States President and Vice President', '', 9901, 'Write-in', '10/28/2016 6:53:36 PM', 1, 149, 0.0909090909090909, '837/1311')]
            ]
            '''

            region_list = ['National', 'Oregon', 'Eugene/Springfield', 'Lane County', 'Region']
            for region in region_list:
                obj, created = Region.objects.get_or_create(name=region,
                               defaults={'name': region})

            for contest_item in out_list:
                wrapper, position = ('', '')
                try:
                    wrapper, position = contest_item[1][0][1].split(',', 1)
                    wrapper = wrapper.replace('Commissioner', '').strip()
                    wrapper = wrapper.replace('Director', '').strip()
                    position = position.strip()
                except ValueError:
                    wrapper = contest_item[1][0][1].strip()
                    position = ''

                # Fix stuff like "LINN SOIL AND WATER CONSERVATION DISTRICT"
                if wrapper.isupper():
                    wrapper = wrapper.title()

                new_contest, created = Contest.objects.get_or_create(
                    contest_number=contest_item[1][0][0],
                    defaults={
                        'name': contest_item[1][0][1],
                        'precincts': contest_item[1][0][9].split('/')[1],
                        'precincts_counted': contest_item[1][0][9].split('/')[0],
                        'region_id': csv_file_name['region_id'], # Default to Lane County
                        'print_only': True,
                    }
                )
                if created:
                    # A Contest can exist twice: Once in the Lane County results
                    # and once in the Statewide, i.e. President or Governor,
                    # but we don't want to enter it twice in our Contest
                    # collection, so we check if we already have it. If it's
                    # new, so let's add & populate it, if not, we already
                    # had it, so we can skip it.
                    new_contest.save()
                    c = new_contest.id

                    if wrapper:
                        cw, created = Contest_wrapper.objects.get_or_create(name=wrapper)
                        new_contest.contest_wrapper = cw
                        new_contest.name = position
                        new_contest.save()

                    d = Contest.objects.get(pk = c)
                    for contest_details in contest_item[1]:
                        if contest_details[2]:
                            affiliation = AFFILIATION_LOOKUP.get(contest_details[2], '')
                        else:
                            affiliation = ''
                        if contest_details[4].isupper():
                            a_contest_name = contest_details[4].lower()
                        else:
                            a_contest_name = contest_details[4]
                        d.cand_yes_no_set.create(
                            contest = d,
                            name = a_contest_name,
                            candidate_number = int(contest_details[0]),
                            affiliation = affiliation,
                            incumbent = False,
                        )
