from django.contrib import admin

from councils_members.models import MemberCouncil, Council


class CouncilAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('region__title', 'type')


class MemberCouncilAdmin(admin.ModelAdmin):
    search_fields = ('name', 'council__title')
    raw_id_fields = ('council', 'declaration')
    exclude = ('citizenship', 'party', 'education')


admin.site.register(Council, CouncilAdmin)
admin.site.register(MemberCouncil, MemberCouncilAdmin)
