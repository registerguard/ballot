import hashlib

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.http import HttpRequest
from django.template import resolve_variable
from django.utils.http import urlquote
from django.utils.cache import _generate_cache_header_key


class Command(BaseCommand):
    help = '''
    Clears the cache for /ballot/results/full
    '''

    def handle(self, *args, **options):
        # Deletes hard-wired 'main_results_table' fragment from main results
        args = hashlib.md5(u':'.join([urlquote(u'')]))
        cache_key = 'template.cache.%s.%s' % ('main_results_table', args.hexdigest())
        self.stdout.write(u'Was there a page fragment cache? {0}\n'.format(cache.has_key(cache_key)))
        cache.delete(cache_key)
        self.stdout.write(u'Cleared the main_results_table fragment!\n')

        # Hard-wire delete of page URL /ballot/results/full/
        request = HttpRequest()
        key_prefix = ''
        request.path = '/ballot/results/full/'
        key = _generate_cache_header_key(key_prefix, request)
        self.stdout.write(u'Was there a URL cache? {0}\n'.format(cache.has_key(key)))
        cache.set(key, None, 0)
        self.stdout.write(u'Cleared the /ballot/results/full/ URL!\n')
