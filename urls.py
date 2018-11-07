from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.views.decorators.cache import cache_page
from ballot.management.commands.ballot_settings import ELECTION_DISPLAY_STRING
from ballot.models import Contest
from ballot.views import json_results, json_wire_stories


'''
Better for primaries:
'queryset': Contest.objects.order_by('region', 'contest_wrapper', 'contest_number',),

Better for general election:
'queryset': Contest.objects.order_by('region', 'contest_number', 'contest_wrapper', 'name',),

REMEMBER:  You can set the order of the races via the Hard-coded Order
part of the Contest Wrapper item, which you're probably going to need in the
case of a primary as the County groups results by party and not race, as we do.
'''
info_dict = {
    'queryset': Contest.objects.filter(print_only=True).order_by('region', 'contest_wrapper__hard_coded_order', 'contest_wrapper', 'name',),
#     'queryset': Contest.objects.order_by('region', 'contest_number', 'contest_wrapper', 'name',),
#     'queryset': Contest.objects.order_by('region', 'contest_number', 'contest_wrapper',),
    'template_name': 'ballot/web_full_list.html',
    'extra_context': {
        'object': {'author': 'John Heasly'},
        'election_title': ELECTION_DISPLAY_STRING,
        },
}

urlpatterns = patterns('',
    # May 19, 2015 special election
    (r'^20150519/print/$', 'ballot.views.print_file'),

    # May 18, 2010 primary
    (r'^20100518/print/$', 'django.views.generic.list_detail.object_list', dict(info_dict, template_name='ballot/20100518-print.html', mimetype='text/plain; charset=UTF-8')),

    # May 15, 2012 primary
    # May 17, 2016 primary
   (r'^20160517/print/$', 'django.views.generic.list_detail.object_list', dict(info_dict, template_name='ballot/20160517-print.html', mimetype='text/plain; charset=UTF-8')),
#    (r'^20120515/print/$', 'django.views.generic.list_detail.object_list', dict(info_dict, template_name='ballot/20100518-print.html', mimetype='text/plain; charset=UTF-8')),

    (r'^results/print/$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^results/check/$', 'django.views.generic.list_detail.object_list', dict({'queryset': Contest.objects.order_by('region', 'contest_wrapper', 'contest_number',)}, template_name='ballot/check_list.html')),

    (r'^results/web/$', object_list, dict({'queryset': Contest.objects.filter(web_front=True).order_by('contest_wrapper__hard_coded_order', 'region', 'contest_wrapper', 'name',)}, template_name='ballot/web_list_gh.html')),
#     (r'^results/web/$', object_list, dict({'queryset': Contest.objects.filter(web_front=True).order_by('contest_wrapper__hard_coded_order', 'contest_number',)}, template_name='ballot/web_list.html')),
#     (r'^results/web/$', cache_page(object_list, 60 * 30), dict({'queryset': Contest.objects.order_by('-contest_number',)}, template_name='ballot/web_list.html')),

    (r'^results/web/test/$', 'django.views.generic.list_detail.object_list', dict({'queryset': Contest.objects.order_by('contest_number',)}, template_name='ballot/web_list_test.html')),

    (r'^results/full/$', cache_page(object_list, 60 * 15), info_dict),

    (r'^results/box/$', 'ballot.views.box_print'),
    (r'^results/box/check/$', 'ballot.views.box_web'),
    (r'^results/main/$', 'ballot.views.main_print'),
    (r'^results/main/check/$', 'ballot.views.main_web'),

    (r'^results/ghm/$', 'ballot.views.ghm_raw'),
    (r'^results/ghm/ic/$', 'ballot.views.ghm_incopy'),

    (r'^json/$', json_results),
    (r'^json/(?P<geo>[a-z]{6})/$', json_results),
    (r'^json/ap_elex_stories/(?P<story_count>\d\d?)/$', json_wire_stories),
)
