from __future__ import division
from django.core.cache import cache
from django.db import models
from django.http import HttpRequest
from django.utils.cache import _generate_cache_header_key
from ballot.templatetags.humanize_list import humanize_list

# Create your models here.

class CCOnSaveBase(models.Model):
    '''
    Apparently stands for Cache Clear On Save. I wonder where I got this?
    In any event, I've backed it out.
    '''
    
    class Meta:
        abstract = True
    
    def delete(self, *args, **kwargs):
        cache.clear()
        super(CCOnSaveBase, self).delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        # Code Smell; hard-wiring these URLs for clearing view caches on save()
        # Better way ('cept for maybe the signal part ... ):
        # http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
        request = HttpRequest()
        key_prefix = ''
        
        json_views = (
            '/ballot/json/',
            '/ballot/json/eugspr/',
            '/ballot/json/laneco/',
            '/ballot/json/region/',
            '/ballot/json/laneme/',
            '/ballot/json/stater/',
            '/ballot/json/statem/',
            '/ballot/json/topset/',
         )
        for json_view in json_views:
            request.path = json_view
            key = _generate_cache_header_key(key_prefix, request)
            if cache.has_key(key):
                cache.set(key, None, 0)
        super(CCOnSaveBase, self).save(*args, **kwargs)

class Region(models.Model):
    name = models.CharField(max_length=300, blank=True)
    
    class Meta:
        ordering = ('id',)
    
    def __unicode__(self):
        return self.name

class Contest_wrapper(models.Model):
    name = models.CharField(max_length=290)
    hard_coded_order = models.IntegerField(u'hard-coded order', default=0)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class Contest(models.Model):
    region = models.ForeignKey(Region)
    contest_wrapper = models.ForeignKey(Contest_wrapper, null=True, blank=True)
    name = models.CharField(max_length=285, blank=True)
    explainer_text = models.TextField(blank=True)
    contest_number = models.IntegerField(blank=True, null=True)
    precincts = models.IntegerField(blank=True, null=True)
    precincts_counted = models.IntegerField(blank=True, null=True)
    party_code = models.CharField(max_length=4, blank=True)
    district_category = models.CharField(max_length=22, blank=True)
    print_only = models.BooleanField(u'Use in paper?', default=True)
    statewide = models.BooleanField(blank=True)
    web_front = models.BooleanField(blank=True)
    is_race = models.BooleanField(blank=True, default=True, help_text=u"If unchecked, then this Contest is a Measure.")
    short_contest_description = models.CharField(max_length=32, blank=True)
    
    class Meta:
#         order_with_respect_to = 'contest_number'
#         ordering = ('contest_number', 'name',)
        ordering = ('contest_number',)
#         unique_together = ('contest_wrapper','name',)
    
    def __unicode__(self):
        return '%s %s' % ( getattr(self.contest_wrapper, "name", ""), getattr(self, "name", "") )
    
    def contestants(self):
        return humanize_list([ item.name for item in self.cand_yes_no_set.all() ])
    
    def exclude_odd_bits(self):
        return self.cand_yes_no_set.exclude(name='Write-in').exclude(name='over votes').exclude(name='under votes')
    
    def no_one_filed(self):
        from sets import Set
        a = Set([ item.name for item in self.cand_yes_no_set.all() ])
        b = Set([u'under votes', u'write-in', u'over votes'])
        if not a.difference(b):
            return True # no one filed for the race
        else:
            return False
    
    def measure(self):
        candidate_list = [cand.name for cand in self.cand_yes_no_set.all()]
        if u'Yes' in candidate_list:
            return True
        else:
            return False
    
    def local_vote_total(self):
        vote_total = 0
        for each_cand in self.cand_yes_no_set.all():
            # Filter out 'over votes' and 'under votes'!
            if each_cand.votes_local and not 'votes' in each_cand.name:
                vote_total = vote_total + each_cand.votes_local
            else:
                vote_total = vote_total + 0
        return vote_total
    
    def other_vote_total(self):
        vote_total = 0
        for each_cand in self.cand_yes_no_set.all():
            if each_cand.votes_other:
                vote_total = vote_total + each_cand.votes_other
            else:
                vote_total = vote_total + 0
        return vote_total

# class Cand_yes_no(CCOnSaveBase):
class Cand_yes_no(models.Model):
    POLITICAL_PARTY = (
    ('C',  'Constitution'),
    ('D',  'Democrat'),
    ('I',  'Independent'),
    ('L',  'Libertarian'),
    ('N',  'Nonpartisan'),
    ('PR', 'Progressive'),
    ('P',  'Peace'),
    ('PG', 'Pacific Green'),
    ('R',  'Republican'),
    ('WF', 'Working Families'),
    )
    
    contest = models.ForeignKey(Contest)
    name = models.CharField(u"Candidate's name or Yes/No", max_length = 400)
    candidate_number = models.IntegerField(editable=False, null=True)
    affiliation = models.CharField(max_length=56, choices=POLITICAL_PARTY, blank=True)
    votes_local = models.IntegerField(null=True, blank=True)
    votes_other = models.IntegerField(null=True, blank=True)
    votes_national = models.IntegerField(null=True, blank=True)
    incumbent = models.BooleanField(blank=True)
    extra_cand_meas_text = models.TextField(blank=True)
    image_url = models.CharField(max_length=300, blank=True)
    
    class Meta:
        ordering = ('-votes_other', '-votes_local', 'candidate_number',)
    
    def __unicode__(self):
        return self.name
    
    def unopposed(self):
        pass
    
    def local_percent(self):
        try:
#             return '%2.2f' % ((self.votes_local / self.contest.local_vote_total()) * 100)
            return '{0:.2f}'.format( self.votes_local / self.contest.local_vote_total() * 100 ).rstrip('0')
        except (ZeroDivisionError, TypeError):
            return 0
    
    def other_percent(self):
        try:
#             return '%2.2f' % ((self.votes_other / self.contest.other_vote_total()) * 100)
            return '{0:.2f}'.format( self.votes_other / self.contest.other_vote_total() * 100 ).rstrip('0')
        except (ZeroDivisionError, TypeError):
            return 0
    
    def candidate_or_decision(self):
        '''
        To filter out vote totals of
            "over vote"
            "under vote" and
            "write-in"
        from Lane County election results
        '''
        if not self.name.startswith('over') and \
        not self.name.startswith('under') and \
        not self.name.startswith('write'):
            return True
        else:
            return False
