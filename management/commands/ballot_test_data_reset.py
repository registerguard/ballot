from ballot.models import Cand_yes_no
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        cand_meas_list = Cand_yes_no.objects.all()
        for cand_meas in cand_meas_list:
            cand_meas.votes_local = 0
            cand_meas.votes_other = 0
            cand_meas.save()
            print '%s %s zeroed out.' % (cand_meas.contest.contest_wrapper, cand_meas.name)
            