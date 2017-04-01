from django.contrib import admin

from councils_members.models import Person, Council


class CouncilAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('region__title', 'type')


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'council__title')
    raw_id_fields = ('council', 'declaration')


admin.site.register(Council, CouncilAdmin)
admin.site.register(Person, PersonAdmin)
