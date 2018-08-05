# Create your views here.
import datetime
import json
import random
import string

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from rest_framework.decorators import throttle_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from urlshortner.decorators import validate_url
from urlshortner.models import UrlKeyHash


def home(request):
    return index(request)


@api_view(['GET'])
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


@api_view(['POST'])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@validate_url
def make_tiny_url(request):
    long_url = request.POST.get('url')
    is_private = request.POST.get('is_private', False)
    custom_key = request.POST.get('custom_key')
    expired_on = request.POST.get('expire_on')
    if not custom_key:
        custom_key = get_short_hash()
    else:
        if not (custom_key_available(custom_key) or len(custom_key) < 10):
            return HttpResponse(json.dumps({'error': 'Custom key not available or too long'}), status=400, content_type='application/json')

    expired_on_date = None
    if expired_on:
        expired_on_date = datetime.datetime.strptime(expired_on, '%Y-%m-%d').date()
        if (expired_on_date - datetime.date.today()).total_seconds() < 0:
            return HttpResponse(json.dumps({'error': 'Please select future date'}), content_type='application/json')

    UrlKeyHash.objects.create(url=long_url, key=custom_key, is_private=is_private, expired_on=expired_on_date)
    short_url = '{}/{}'.format(settings.SITE_URL, custom_key)
    return HttpResponse(json.dumps({'short_url': short_url}), content_type='application/json')


def index(request):
    ctxt = {}
    urls = UrlKeyHash.objects.order_by('-created_on').all()
    ctxt.update(csrf(request))
    paginator = Paginator(urls, 10)
    page = request.GET.get('page', 1)
    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        urls = paginator.page(1)
    except EmptyPage:
        urls = paginator.page(paginator.num_pages)

    ctxt['urls'] = urls
    return render(request, 'index.html', ctxt)
