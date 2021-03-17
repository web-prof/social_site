from django.contrib import admin
from .models import *

admin.site.site_header = "social"
admin.site.index_title = "index_social"
admin.site.site_title = "mytitle"



admin.site.register(Profile)
admin.site.register(Relationship)