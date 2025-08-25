from django.contrib import admin

from .models import *

admin.site.register(Source)
admin.site.register(Quote)
admin.site.register(PageViews)