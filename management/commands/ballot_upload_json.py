from django.core.management.base import BaseCommand, CommandError

import boto3
import requests

import os

URLS = (
    'http://projects.registerguard.com/ballot/json/',
    'http://projects.registerguard.com/ballot/json/eugspr/',
    'http://projects.registerguard.com/ballot/json/laneco/',
    'http://projects.registerguard.com/ballot/json/region/',
    'http://projects.registerguard.com/ballot/json/laneme/',
    'http://projects.registerguard.com/ballot/json/stater/',
    'http://projects.registerguard.com/ballot/json/statem/',
    'http://projects.registerguard.com/ballot/json/topset/',
)

JSON_DIRECTORY = 'json'

FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        for url in URLS:
            r = requests.get(url)
            with open(os.path.join(FILE_PATH, JSON_DIRECTORY, '{0}.json'.format(url.split('/')[-2])), 'wb+') as json_file:
                json_file.write(r.content)
