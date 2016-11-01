from ballot.management.commands.ballot_settings import CSV_DIRECTORY,\
    CSV_FILE_NAMES, LANE_CONTEST_IDS
from ballot.models import Cand_yes_no

from django.core.management.base import BaseCommand, CommandError

import csv
import os


class Command(BaseCommand):
    help = ''''''

    def handle(self, *args, **options):
        for csv_file_name in CSV_FILE_NAMES:
            with open(os.path.join(CSV_DIRECTORY, csv_file_name['file']), 'rb') as results_in:
                results_reader = csv.reader(results_in)
                next(results_reader, None) # skip the headers
                for result_row in results_reader:
                    # only process SOS results we're interested in!
                    if csv_file_name['check_if_needed']:
                        if int(result_row[0]) in LANE_CONTEST_IDS:
                            contest_name,\
                            contestant_name,\
                            contest_number,\
                            candidate_number,\
                            total_precincts,\
                            precincts_counted,\
                            votes_other = result_row[1],\
                            result_row[8],\
                            int(result_row[0]),\
                            int(result_row[7]),\
                            int(result_row[13].split('/')[1]),\
                            int(result_row[13].split('/')[0]),\
                            int(result_row[11])

                            self.stdout.write('''Contest name:{0}
Contestant: {1}
Contest number: {2}
Candidate number: {3}
Total precincts: {4}
Precincts counted: {5}
Votes! {6}\n'''.format(contest_name,\
                            contestant_name,\
                            contest_number,\
                            candidate_number,\
                            total_precincts,\
                            precincts_counted,\
                            votes_other))

                            contestant_to_update = Cand_yes_no.objects.get(
                                contest__contest_number=contest_number,
                                candidate_number=candidate_number,
                            )
                            contestant_to_update.votes_other = votes_other
                            contestant_to_update.save()

                            if precincts_counted:
                                contestant_to_update.contest.precincts_counted = precincts_counted
                                contestant_to_update.save()

                            self.stdout.write('''Updating {0} of {1}
    ... {2} votes ...\n'''.format(contestant_name, contest_name, votes_other))
                    else:
                        # It's from Lane County! Process every .csv row!
                        contest_name,\
                        contestant_name,\
                        contest_number,\
                        candidate_number,\
                        total_precincts,\
                        precincts_counted,\
                        lane_votes = result_row[1],\
                        result_row[8],\
                        int(result_row[0]),\
                        int(result_row[7]),\
                        int(result_row[13].split('/')[1]),\
                        int(result_row[13].split('/')[0]),\
                        int(result_row[11])

                        self.stdout.write('''Contest name:{0}
Contestant: {1}
Contest number: {2}
Candidate number: {3}
Total precincts: {4}
Precincts counted: {5}
Votes! {6}\n'''.format(contest_name,\
                        contestant_name,\
                        contest_number,\
                        candidate_number,\
                        total_precincts,\
                        precincts_counted,\
                        lane_votes))

                        contestant_to_update = Cand_yes_no.objects.get(
                            contest__contest_number=contest_number,
                            candidate_number=candidate_number,
                        )
                        contestant_to_update.votes_local = lane_votes
                        contestant_to_update.save()

                        if precincts_counted:
                            contestant_to_update.contest.precincts_counted = precincts_counted
                            contestant_to_update.save()

                        self.stdout.write('''Updating {0} of {1}
    ... {2} votes ...\n'''.format(contestant_name, contest_name, lane_votes))

        self.stdout.write('''Done parsing {0} that were in {1}
'''.format([i['file'] for i in CSV_FILE_NAMES], CSV_DIRECTORY))
