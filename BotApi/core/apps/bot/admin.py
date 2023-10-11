from django.contrib import admin
from .models import *

for name, obj in models.__dict__.items():
    if isinstance(obj, type) and isinstance(obj, models.Model):
        admin.site.register(obj)
