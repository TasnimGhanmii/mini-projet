from django.contrib import admin
from .models import Professor, Session, Formula

admin.site.register(Professor)
admin.site.register(Session)
admin.site.register(Formula)