from django.contrib.humanize.templatetags.humanize import intcomma
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.serializers import get_serializer
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson
from django.utils.dateformat import DateFormat
# from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_list

from ap_wfm.models import APStory
from ballot.models import Contest
from cuddlybuddly.storage.s3.exceptions import S3Error
from fancy_cache import cache_page
from sorl.thumbnail import get_thumbnail

import datetime

# Create your views here.

def box_web(request):
    return object_list(
        request,
        queryset = Contest.objects.filter(Q(region__name='National') | Q(region__name='Oregon')).exclude(name__regex=r'^\d\d\d?$').order_by('region__name', 'contest_number'),
#         queryset = Contest.objects.filter(region__name='National and State').order_by('region__name', 'contest_number'),
        template_name = 'ballot/box_list_check.html',
        extra_context = {
            'state_measures_list': lambda: Contest.objects.filter(name__regex=r'^\d\d\d?$').order_by('name',),
            'lane_measures_list' : lambda: Contest.objects.filter(name__startswith='20-'),
#             'regional_measures_list' : lambda: Contest.objects.filter(region__name='National and State').order_by('-contest_wrapper__name', 'name'),
            'regional_measures_list' : lambda: Contest.objects.filter(name__regex=r'^(6|10|21|)\-\d+').order_by('region__name', 'name'),
        }
    )

def box_print(request):
    queryset = Contest.objects.filter(Q(region__name='National') | Q(region__name='Oregon')).exclude(name__regex=r'^\d\d\d?$').order_by('region__name', 'contest_number')
    t = loader.get_template('ballot/box_list.html')
    c = RequestContext(request,
        {
            'object_list': queryset,
            'state_measures_list': lambda: Contest.objects.filter(name__regex=r'^\d\d\d?$').order_by('contest_number',),
            'lane_measures_list' : lambda: Contest.objects.filter(name__startswith='20-').order_by('contest_number',),
            'regional_measures_list' : lambda: Contest.objects.filter(name__regex=r'^(6|10|21|)\-\d+').order_by('region__name', 'name'),
        }
    )
    data = t.render(c)
    data = data.encode('utf-16-le')
    r = HttpResponse(data, mimetype='text/plain;charset=utf-16le')
    r['Content-Disposition'] = 'attachment; filename=box.txt;'
    return r

#     return object_list(
#         request,
#         queryset = Contest.objects.filter(Q(region__name='National') | Q(region__name='Oregon')).exclude(name__regex=r'^\d\d$').order_by('region__name', 'contest_number'),
# #         queryset = Contest.objects.filter(region__name='National and State').exclude(name__regex=r'^7\d+').order_by('region__name', 'contest_number'),
#         template_name = 'ballot/box_list.html',
#         extra_context = {
#             'state_measures_list' : lambda: Contest.objects.filter(name__regex=r'^\d\d$').order_by('name',),
#             'lane_measures_list' : lambda: Contest.objects.filter(name__startswith='20-').order_by('name',),
# #             'regional_measures_list' : lambda: Contest.objects.filter(region__name='National and State').order_by('-contest_wrapper__name', 'name'),
# #             'regional_measures_list' : lambda: Contest.objects.filter(name__regex=r'^(6|10|21|)\-\d+').order_by('region'),
#         }
#     )

def main_web(request):
    return object_list(
        request,
#         queryset = Contest.objects.filter(region__name='Lane County').filter(print_only=True).order_by('contest_number'),
        queryset = Contest.objects.filter(region__name='Lane County').filter(print_only=True).order_by('contest_wrapper__name'),
        template_name = 'ballot/main_list_check.html',
        extra_context = {
#             'benton_county' : lambda: Contest.objects.filter(region__name='Benton County').order_by('contest_number'),
#             'coos_county' : lambda: Contest.objects.filter(region__name='Coos County').order_by('contest_number'),
#             'douglas_county' : lambda: Contest.objects.filter(region__name='Douglas County').order_by('contest_number'),
#             'lincoln_county' : lambda: Contest.objects.filter(region__name='Lincoln County').order_by('contest_number'),
#             'linn_county' : lambda: Contest.objects.filter(region__name='Linn County').order_by('contest_number'),
            'benton_county' : lambda: Contest.objects.filter(region__name='Benton County').order_by('contest_wrapper__name', 'name'),
            'coos_county' : lambda: Contest.objects.filter(region__name='Coos County').order_by('contest_wrapper__name', 'name'),
            'douglas_county' : lambda: Contest.objects.filter(region__name='Douglas County').order_by('contest_wrapper__name', 'name'),
            'lincoln_county' : lambda: Contest.objects.filter(region__name='Lincoln County').order_by('contest_wrapper__name', 'name'),
#             'linn_county' : lambda: Contest.objects.filter(region__name='Linn County').order_by('contest_number'),
            'region': lambda: Contest.objects.filter(region__name='Region').exclude(is_race=False),
        }
    )

'''
def main_print(request):
    return object_list(
        request,
        queryset = Contest.objects.filter(region__name='Lane County').filter(print_only=True, contest_wrapper__isnull=False).order_by('contest_wrapper', 'name'),
#         queryset = Contest.objects.filter(print_only=True).order_by('contest_number'),
        template_name = 'ballot/main_list.html',
        extra_context = {
            'benton_county' : lambda: Contest.objects.filter(region__name='Benton County', print_only=True, contest_wrapper__isnull=False).order_by('contest_wrapper', 'name'),
            'coos_county' : lambda: Contest.objects.filter(region__name='Coos County', print_only=True, contest_wrapper__isnull=False).order_by('contest_wrapper', 'name'),
            'douglas_county' : lambda: Contest.objects.filter(region__name='Douglas County', print_only=True, contest_wrapper__isnull=False).order_by('contest_wrapper', 'name'),
            'lincoln_county' : lambda: Contest.objects.filter(region__name='Lincoln County', print_only=True, contest_wrapper__isnull=False).order_by('contest_wrapper', 'name'),
#             'linn_county' : lambda: Contest.objects.filter(region__name='Linn County').order_by('contest_number'),
        }
    )
'''

def main_print(request):
    queryset = Contest.objects.filter(region__name='Eugene/Springfield').filter(print_only=True, contest_wrapper__isnull=False).exclude(name__regex=r'^\d\d\-').order_by('contest_wrapper', 'name')
    t = loader.get_template('ballot/main_list.html')
    c = RequestContext(request,
        {
            'object_list': queryset,
            'lane_county': lambda: Contest.objects.filter(region__name='Lane County', print_only=True, contest_wrapper__isnull=False).exclude(name__regex=r'^\d\d\d?').order_by('contest_wrapper', 'name'),
            'measures': lambda: Contest.objects.filter(region__name='Measures').exclude(is_race=False).order_by('contest_wrapper', 'name'),
            'benton_county': lambda: Contest.objects.filter(region__name='Benton County').exclude(is_race=False).order_by('contest_wrapper', 'name'),
            'lincoln_county': lambda: Contest.objects.filter(region__name='Lincoln County').exclude(is_race=False).order_by('contest_wrapper', 'name'),
            'linn_county': lambda: Contest.objects.filter(region__name='Linn County').exclude(is_race=False).order_by('contest_wrapper', 'name'),
        }
    )
    data = t.render(c)
    data = data.encode('utf-16-le')
    r = HttpResponse(data, mimetype='text/plain;charset=utf-16le')
    r['Content-Disposition'] = 'attachment; filename=main.txt;'
    return r

#     return object_list(
#         request,
#         queryset = Contest.objects.filter(region__name='Eugene/Springfield').filter(print_only=True, contest_wrapper__isnull=False).exclude(name__regex=r'^\d\d\-').order_by('contest_wrapper', 'name'),
# #         queryset = Contest.objects.filter(print_only=True).order_by('contest_number'),
#         template_name = 'ballot/main_list.html',
#         extra_context = {
#             'lane_county' : lambda: Contest.objects.filter(region__name='Lane County', print_only=True, contest_wrapper__isnull=False).exclude(name__regex=r'^\d\d+').order_by('contest_wrapper', 'name'),
#         }
#     )

def print_file(request):
    # Hoops jumped through to encode response
    queryset = Contest.objects.order_by('region', 'contest_number', 'contest_wrapper', 'name',)
    template_name = 'ballot/20150519-print.html'
    mimetype = 'text/plain'
    t = loader.get_template(template_name)
    c = RequestContext(request, {'object_list': queryset })
    data = t.render(c)
    data = data.encode('utf-16le')
    resp = HttpResponse(data, mimetype=mimetype)
    resp['Content-Disposition'] = 'attachment; filename=election-results.txt'
    return resp

# @cache_page(15 * 60, only_get_keys=['floobert'])
def json_results(request, geo=None, **kwargs):

    queryset = []
    race_queryset = []
    meas_queryset = []
    queryset_dict = {}

    # Check for region-specific URL request
    if geo:
        geography = geo

        # Eugene/Springfield races
        if geography == 'eugspr':
            queryset = Contest.objects.filter(region__name='Eugene/Springfield').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # Lane County races
        if geography == 'laneco':
            queryset = Contest.objects.filter(region__name='Lane County').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # Any non-state, non-Lane County races, measures we cover
        if geography == 'region':
            queryset = Contest.objects.filter(region__name='Region').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # Lane County measures
        if geography == 'laneme':
            # I've built two ways, apparently, to filter for Measures, the 'region__name' and 'is_race' column. So ...  
            queryset = Contest.objects.filter(is_race=False, contest_wrapper__name__startswith='20-').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # State races; Lane County votes, state votes
        if geography == 'stater':
            queryset = Contest.objects.filter(statewide=True).exclude(name__regex=r'^\d\d\d?$').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # State measures; Lane County votes, state votes
        if geography == 'statem':
            queryset = Contest.objects.filter(statewide=True, name__regex=r'^\d\d\d?$').order_by('contest_wrapper__hard_coded_order', 'contest_number')
            queryset_dict['options'] = queryset

        # Top two races, top three measures
        if geography == 'topset':
            race_queryset = Contest.objects.filter(is_race=True, web_front=True)
            meas_queryset = Contest.objects.filter(is_race=False, web_front=True)
            queryset_dict['race'] = race_queryset
            queryset_dict['measure'] = meas_queryset

    else:
        queryset = Contest.objects.filter(contest_wrapper__isnull=False).order_by('contest_wrapper', 'name')
        queryset_dict['options'] = queryset

    json_list = []
    wrap_json_list = []
    '''
    queryset_dict =
    {
        'measure': [<Contest: State Measure 90>, <Contest: State Measure 91>, <Contest: State Measure 92>],
        'race': [<Contest: U.S. Senate >, <Contest: Governor >]
    }
    '''
    for contest_key in queryset_dict.keys():
        for contest_queryset in queryset_dict[contest_key]:
            cand_yes_no_list = []
            for cand_yes_no in contest_queryset.cand_yes_no_set.all():
                cand_yes_no_list.append({
                                        'name': cand_yes_no.name,
                                        'cand_meas_id': cand_yes_no.id,
                                        'lane_votes': intcomma(cand_yes_no.votes_local),
                                        'statewide_issue': contest_queryset.statewide,
                                        'state_votes': intcomma(cand_yes_no.votes_other),
                                        'incumbent': cand_yes_no.incumbent,
                                        'percent_of_lane_votes': cand_yes_no.local_percent(),
                                        'percent_of_state_votes': cand_yes_no.other_percent(),
                                        'affiliation': cand_yes_no.affiliation,
                                        'affiliation_pretty': cand_yes_no.get_affiliation_display(),
                                        'image_url': cand_yes_no.image_url,
                                        'extra_text': cand_yes_no.extra_cand_meas_text
                                        })
            json_list.append({
                             'updated': datetime.datetime.now().strftime('%c'),
                             'contest_wrapper': getattr(contest_queryset.contest_wrapper, "name", ""),
                             'contest_name': contest_queryset.name,
                             'contest_id': contest_queryset.id,
                             'explainer_text': contest_queryset.explainer_text,
                             'short_description': contest_queryset.short_contest_description,
                             'web_front': contest_queryset.web_front,
                             contest_key: cand_yes_no_list
                             })

        if len(queryset_dict.keys()) > 1:
            # More than one key means a 'measure', 'race' combination keyed
            # dictionary for the top of the page
            wrap_json_list.append({
                                '%s%s' % (contest_key, 's'): json_list
                             })
            # Clean out the list for the next contest_key
            json_list = []
        else:
            wrap_json_list = json_list

#     json_data = simplejson.dumps(json_list, indent=2)
    json_data = simplejson.dumps(wrap_json_list, indent=2)

    callback = request.GET.get('callback')
    if callback:
        response = HttpResponse('%s(%s)' % (callback, json_data), mimetype='application/javascript')
    else:
        response = HttpResponse(json_data, mimetype='application/javascript')
    return response


def add_junk(response, request):
    # pull from cache (if there is a cached response)
    junk = response.content
    if "(" in junk:
        callback, data = junk.split("(")
        # overwrite cached callback value with new callback value
        callback = request.GET.get('callback', default='')
        newjunk = '%s(%s' % (callback, data)
        response.content = newjunk
    return response

@cache_page(5 * 60, only_get_keys=['floobert'], post_process_response_always=add_junk)
def json_wire_stories(request, **kwargs):
    current_site = Site.objects.get(id=settings.SITE_ID)

    if 'story_count' in kwargs:
        story_count = kwargs['story_count']
    else:
        story_count = 5
    # queryset = APStory.objects.filter(category=23, consumer_ready=True, slug__regex=r'^us-+|or-+|wa-+|id-+')[:story_count]
    queryset = APStory.objects.filter(category=23, consumer_ready=True, slug__regex=r'^[uowi][srad]-+').exclude(slug__endswith='-trend')[:story_count]

    story_list = []
    for story in queryset:
        first_image_thumb = None
        if story.location and ',' in story.location:
            dateline_city, dateline_state = story.location.split(', ')
        else:
            dateline_city = story.location
            dateline_state = ''

        dateline_city.strip()
        dateline_state.strip()

        try:
            if story.image_set.all():
                first_image_thumb = get_thumbnail(story.image_set.all()[0].image, '200x200', quality=85)
        except S3Error, err:
            print err

        story_list.append({
                          'dateline_city': dateline_city,
                          'dateline_state': dateline_state,
                          'dateline': story.location,
                          'headline': story.headline,
                          'story_url': 'http://%s%s' % ( current_site.domain, reverse('ap_story_detail', args=[story.category.all()[0].name, story.slug]) ),
                          'updated': DateFormat(story.updated).format('c'),
                          'first_image_thumb_url': getattr(first_image_thumb, 'url', '')
                          })
    json_data = simplejson.dumps(story_list, indent=2)



    callback = request.GET.get('callback')
    if callback:
        response = HttpResponse('%s(%s);' % (callback, json_data), mimetype='application/javascript; charset=utf-8')
        response['Cache-Control'] = 'no-cache'
    else:
        response = HttpResponse(json_data, mimetype='application/javascript; charset=utf-8')
    return response

def ghm_raw(request):
    return object_list(
        request,
        queryset = Contest.objects.filter(print_only=True, is_race=True).order_by('region', 'contest_wrapper__hard_coded_order', 'contest_number'),
        template_name='ballot/ghm_raw.html',
        extra_context = {
            'measures_list': lambda: Contest.objects.filter(print_only=True, is_race=False).order_by('region', 'name'),
        }
    )

def ghm_incopy(request):
    queryset = queryset = Contest.objects.filter(print_only=True, is_race=True).order_by('region', 'contest_number')
    template_name='ballot/ghm_incopy.txt'
    mimetype = 'text/plain'
    t = loader.get_template(template_name)
    c = RequestContext(
        request,
        {
            'object_list': queryset,
            'measures_list': lambda: Contest.objects.filter(print_only=True, is_race=False).order_by('region', '-name'),
        }
    )
    data = t.render(c)
    data = data.encode('utf-16le')
    resp = HttpResponse(data, mimetype=mimetype)
    resp['Content-Disposition'] = 'attachment; filename=election-results.txt'
    return resp
    
