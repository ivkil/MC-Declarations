from django.contrib import admin

from declarations.models import Declaration


class DeclarationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'last_name', 'first_name', 'workplace', 'position', 'residence')
    list_filter = ('checked',)
    readonly_fields = ('checked',)


admin.site.register(Declaration, DeclarationAdmin)
