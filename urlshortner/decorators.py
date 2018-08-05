import json

from django.http import HttpResponse

from urlshortner.url_helper import UrlHelper


def validate_url(function):
    def wrap(request, *args, **kwargs):
        url = request.POST.get('url')
        if not url:
            return HttpResponse(json.dumps({'error': 'url is required'}), content_type='application/json')
        is_valid_url = UrlHelper.is_valid_Url(url)
        if not is_valid_url:
            return HttpResponse(json.dumps({'error': 'Entered url is not valid'}), content_type='application/json')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
