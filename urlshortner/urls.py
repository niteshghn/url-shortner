from django.conf.urls import url

from urlshortner import views

urlpatterns = [
    url(r'', views.home, name='home'),
    url(r'^(?P<hash>\w{6})$', views.redirect_to_source, name='redirect-source'),
    url(r'^make-tiny/$', views.make_tiny_url, name='make-tiny')
]
