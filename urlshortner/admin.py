from django.contrib import admin

# Register your models here.
from urlshortner.models import UrlKeyHash

admin.site.register(UrlKeyHash)