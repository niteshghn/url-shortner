from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from urlshortner import views

urlpatterns = [
    url(r'^(?P<hash>\w{6})$', views.redirect_to_source, name='redirect-source'),
    url(r'^make-tiny/$', csrf_exempt(views.make_tiny_url), name='make-tiny'),
    url(r'^home/$', views.home, name='home'),
]
