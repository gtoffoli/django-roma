from __future__ import unicode_literals

def get_focus(request):
    focus = request.session.get("focus", None)
    if not focus:
        focus = {}
    return focus

def set_focus(request, tags=None, klasses=None, zones=None, poi=None, key=None, value=None):
    focus = get_focus(request)
    if key:
        focus[key] = value
    elif tags is not None:
        focus['tags'] = tags
    elif klasses is not None:
        focus['klasses'] = klasses
    elif poi:
        pass
    if zones is not None:
        focus['zones'] = zones
    elif poi:
        pass
    request.session["focus"] = focus

def focus_set_category(request, category):
    klasses = get_focus(request).get('klasses', [])
    if category in klasses:
        klasses.remove(category)
    klasses.append(category)
    set_focus(request, klasses=klasses)

def focus_add_themes(request, themes):
    tags = get_focus(request).get('tags', [])
    for tag in tags:
        if not tag in themes:
            themes.append(tag)
    set_focus(request, tags=themes)
