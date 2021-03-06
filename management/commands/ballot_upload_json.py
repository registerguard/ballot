from ballot.management.commands.ballot_settings import JSON_URLS
from django.core.management.base import BaseCommand, CommandError

import sys

try:
    import boto3
except ImportError:
    sys.exit('This script meant for local use only.')
import requests

import os

LOCAL_JSON_DIRECTORY = 'json'
AWS_JSON_DIRECTORY = 'results'
AWS_BUCKET = 'vote.registerguard.com'

FILE_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__)))

class Command(BaseCommand):
    help = '''Downloads a hard-coded list of URLs that provide json files and
 uploads them to a hard-coded AWS S3 bucket.'''

    def handle(self, *args, **options):
        s3 = boto3.resource('s3')

        for url in JSON_URLS:
            self.stdout.write("Downloading\n    '{0}' ... \n".format(url))
            r = requests.get(url)
            with open(os.path.join(FILE_PATH, LOCAL_JSON_DIRECTORY, '{0}.json'.format(url.split('/')[-2])), 'wb+') as json_file:
                json_file.write(r.content)

        # get the list of files (and _only_ files; os.listdir() gives you directories & files ... ) you just wrote ...
        json_file_list = [f for f in os.listdir(os.path.join(FILE_PATH, LOCAL_JSON_DIRECTORY)) if os.path.isfile(os.path.join(FILE_PATH, LOCAL_JSON_DIRECTORY, f))]

        for json_file in json_file_list:
            self.stdout.write("Uploading\n    '{0}'\n    to '{1}'\n    in AWS S3 bucket '{2}' ... \n".format(
                os.path.join(FILE_PATH, LOCAL_JSON_DIRECTORY, json_file),
                os.path.join(AWS_JSON_DIRECTORY, json_file),
                AWS_BUCKET)
            )
            s3.meta.client.upload_file( os.path.join(FILE_PATH, LOCAL_JSON_DIRECTORY, json_file), AWS_BUCKET, os.path.join(AWS_JSON_DIRECTORY, json_file), ExtraArgs={'ContentType': "application/json", 'ACL': "public-read"} )
