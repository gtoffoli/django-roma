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
        'use_localeurl': settings.USE_LOCALEURL,
    }

    return my_settings
