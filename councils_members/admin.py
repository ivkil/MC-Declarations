from django.contrib import admin
from django.core.management import call_command

from councils_members.models import Person, Council


class CouncilAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('region__title', 'type')


def find_declaration(modeladmin, request, queryset):
    for obj in queryset:
        call_command('mc_find_declaration', obj.id)


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'council__title')
    list_filter = ('active_member_council',)
    raw_id_fields = ('council', 'declaration')
    readonly_fields = ('declaration',)

    actions = [find_declaration]


admin.site.register(Council, CouncilAdmin)
admin.site.register(Person, PersonAdmin)
