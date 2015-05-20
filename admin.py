from django.contrib import admin
from ballot.models import Region, Contest_wrapper, Contest, Cand_yes_no

class ContestInline(admin.TabularInline):
    model = Contest

class RegionAdmin(admin.ModelAdmin):
    model = Region
    inlines = [ContestInline]

admin.site.register(Region, RegionAdmin)

class Contest_wrapperAdmin(admin.ModelAdmin):
    list_display = ('name', 'hard_coded_order',)
    list_editable = ('name', 'hard_coded_order',)

admin.site.register(Contest_wrapper, Contest_wrapperAdmin)

class Cand_yes_noInline(admin.TabularInline):
    model = Cand_yes_no

class ContestAdmin(admin.ModelAdmin):
    model = Contest
    inlines = [Cand_yes_noInline]
    list_display = ('region', 'contest_wrapper', 'name', 'contestants', 'explainer_text', 'short_contest_description', 'district_category', 'print_only', 'contest_number', 'statewide', 'web_front', 'is_race',)
    list_display_links = ('contest_wrapper',)
    list_filter = ('region', 'is_race', 'statewide', 'print_only', 'web_front', 'contest_wrapper',)
    list_editable = ('region', 'name', 'explainer_text', 'short_contest_description', 'district_category', 'print_only', 'statewide', 'web_front', 'is_race',)
    save_on_top = True

admin.site.register(Contest, ContestAdmin)

class Cand_yes_noAdmin(admin.ModelAdmin):
    list_display = ('contest', 'name', 'incumbent',)
    list_filter = ('incumbent',)
    list_editable = ('name', 'incumbent',)
    search_fields = ['name']
    ordering = ('name',)
    save_on_top = True

admin.site.register(Cand_yes_no, Cand_yes_noAdmin)
