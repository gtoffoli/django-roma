from __future__ import unicode_literals
from django.conf import settings

def context_processor(request):
    try:
        show_map = settings.SHOW_MAPS and not request.user_agent.is_bot
    except:
        show_map = False
    my_settings = {
        'site_name': settings.SITE_NAME,
        # 'site_url': request.META['HTTP_HOST'],
        'site_url': request.META.get('HTTP_HOST', 'www.romapaese.it'),
        'map': show_map,
        'maps_key': settings.GOOGLE_MAPS_KEY,
    }

    return my_settings
