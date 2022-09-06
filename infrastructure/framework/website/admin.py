from django.contrib import admin

from infrastructure.framework.website.models import AwsBucket


class AwsBucketAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "url")
    search_fields = ("name",)
    list_filter = ("region",)


admin.site.register(AwsBucket, AwsBucketAdmin)
