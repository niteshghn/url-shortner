# Create your views here.
import json
import random
import string

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from rest_framework.generics import get_object_or_404

from urlshortner.models import UrlKeyHash


def home(request):
    ctxt = {}
    ctxt.update(csrf(request))
    return render(request, 'index.html', ctxt)


def redirect_to_source(request, hash):
    url = get_object_or_404(UrlKeyHash, key=hash)
    url.hits = url.hits + 1
    url.save()
    return HttpResponseRedirect(url.url)


def get_short_hash():
    length = 6
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # check if already exists
    while True:
        code = ''.join(random.choice(char) for x in range(length))
        try:
            UrlKeyHash.objects.get(key=code)
        except UrlKeyHash.DoesNotExist:
            return code


def custom_key_available(custom_key):
    try:
        UrlKeyHash.objects.get(key=custom_key)
        return False
    except UrlKeyHash.DoesNotExist:
        return True


def make_tiny_url(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps({'error': 'Not allowed'}), status=401, content_type='application/json')
    long_url = request.POST.get('url')
    if not long_url:
        return HttpResponse(json.dumps({'error': 'long url is required'}), content_type='application/json')
    is_private = request.POST.get('is_private', False)
    custom_key = request.POST.get('custom_key')
    print(custom_key)
    if not custom_key:
        custom_key = get_short_hash()
    else:
        if not (custom_key_available(custom_key) or len(custom_key) < 10):
            return HttpResponse(json.dumps({'error': 'Custom key not available or too long'}), status=400, content_type='application/json')

    UrlKeyHash.objects.create(url=long_url, key=custom_key, is_private=is_private)
    short_url = '{}/{}'.format(settings.SITE_URL, custom_key)
    return HttpResponse(json.dumps({'short_url': short_url}), content_type='application/json')
