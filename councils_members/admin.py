from django.contrib import admin

from councils_members.models import Person, Council


class CouncilAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_filter = ('region__title', 'type')


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    raw_id_fields = ('council', 'declaration')


class MemberCouncilAdmin(PersonAdmin):
    search_fields = ('name', 'council__title')

    def get_queryset(self, request):
        return self.model.objects.filter(council__isnull=False)


def create_modeladmin(modeladmin, model, name=None):
    class Meta:
        proxy = True
        app_label = model._meta.app_label

    attrs = {'__module__': '', 'Meta': Meta}
    newmodel = type(name, (model,), attrs)
    admin.site.register(newmodel, modeladmin)
    return modeladmin


admin.site.register(Council, CouncilAdmin)
admin.site.register(Person, PersonAdmin)
create_modeladmin(MemberCouncilAdmin, name='members of councils', model=Person)
