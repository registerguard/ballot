import random

from ballot.models import Cand_yes_no
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        cand_meas_list = Cand_yes_no.objects.all()
        for cand_meas in cand_meas_list:
            random_int_local = random.randint(200,10000)
            cand_meas.votes_local = random_int_local
            print 'Lane: %s local votes for %s %s!' % (random_int_local, cand_meas.contest.contest_wrapper, cand_meas.name)
            if cand_meas.contest.statewide:
                random_int_other = random.randint(10000,100000)
                cand_meas.votes_other = random_int_other
                print 'Oregon: %s state votes for %s %s!' % (random_int_other, cand_meas.contest.contest_wrapper, cand_meas.name)
            cand_meas.save()