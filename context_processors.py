from __future__ import unicode_literals
from django.conf import settings

def context_processor(request):
    try:
        show_map = settings.SHOW_MAPS and not request.user_agent.is_bot
    except:
        show_map = False
    try:
        show_element = not request.user_agent.is_bot
    except:
        show_element = True
    my_settings = {
        'site_name': settings.SITE_NAME,
        # 'site_url': request.META['HTTP_HOST'],
        'site_url': request.META.get('HTTP_HOST', 'www.romapaese.it'),
        'map': show_map,
        'show_element': show_element,
        'maps_key': settings.GOOGLE_MAPS_KEY,
        'version_maps' : settings.VERSION_GOOGLE_MAPS,
        'indice_zona' : '/risorse-utili-',
        'recaptcha_key' : settings.GOOGLE_RECAPTCHA_KEY
    }

    return my_settings
