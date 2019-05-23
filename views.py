# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import requests
# import feedparser

from django.core.cache import caches
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext as _
from django.contrib.flatpages.models import FlatPage

import roma.models
from roma.forms import SearchForm, ContactForm
from roma.settings import SERVER_EMAIL, SITE_NAME, ONLINE_DOMAIN, GOOGLE_RECAPTCHA_SKEY
import pois.views
from pois.models import Tag, TagTag, Zone, Poi, Poitype, Confighome
from pois.models import MACROZONE, TOPOZONE, MUNICIPIO
# from roma.fairvillage.api import poitypes as categories


robots_txt = """User-agent: *
Disallow:
"""

def fairvillage(request):
    flatpage = FlatPage.objects.get(pk=32)
    return render(request, 'roma/fairvillage.html', {'text': flatpage.content,})

def robots(request):
    response = render(request, 'roma/robots.txt', {})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    return response

def ads(request):
    response = render(request, 'roma/ads.txt', {})
    response['Content-Type'] = 'text/plain; charset=utf-8'
    return response

def slim(request):
    return render(request, "roma/slim.html", {'text': datetime.datetime.now(),})
    
def generic(request, typ, obj):
    typ = int(typ)
    obj = int(obj)
    if typ == 12:
        return pois.views.zone_detail(request, obj)
    elif typ == 13:
        return pois.views.street_detail(request, obj)
    elif typ == 15:
        return pois.views.poi_detail(request, obj)

def search(request):
    # place holder
    # return render_to_response('search.html')
    if request.method == 'POST': # If the form has been submitted...
        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = SearchForm() # An unbound form
    return render(request, 'search.html', {
        'form': form,
    })

# from django.utils import simplejson
try:
    from django.utils import simplejson
except:
    import json as simplejson

def livesearch(request):
    # called by javascript handler in livesearch.html
    search_qs = roma.models.Search.query(request.REQUEST['search'])
    results = []
    for r in search_qs:
        try:
            d = { 'label': r.title, 'value': '%d,%d' % (r.content_type.id, r.content_object.id) }
            print (d)
            results.append(d)
        except:
            print (r.title, '???')
    print ('N = %d\n' % len(results))
    resp = request.REQUEST['callback'] + '(' + simplejson.dumps(results) + ');'
    return HttpResponse(resp, content_type='application/json')

max_distance = 100
from collections import defaultdict
fixed_points = [
     [100, 150], # salute
     [400,  50], # giovani
     [500, 150], # cultura
     [400, 250], # casa
     [200, 250], # anziani
     [200,  50], # ambiente
]
n_fixed = len(fixed_points)
points = fixed_points

def tags(request):
    """ called by javascript handler in livesearch.html """
    # costruisce la lista dei nodi
    tag_list = Tag.objects.filter(weight__gt=0).order_by('-weight', '-name_it')
    w = 600
    h = 400
    tag_dict = {}
    inverse_tag_dict = {}
    nodes = []
    i = 0
    for tag in tag_list:
        tag_id = tag.id
        name = tag.getName()
        color = tag.color
        node = { 'id': tag_id, 'name': name, 'importance': tag.weight, 'color': color or 'black', 'group': 1,}
        nodes.append(node)
        tag_dict[tag_id] = i
        inverse_tag_dict[i] = tag_id
        print (i, name)
        i += 1
    node_indexes = range(len(tag_dict))
    # inizializza la matrice di connessione
    m = []
    for i in node_indexes:
        r = [max_distance for j in node_indexes]
        m.append(r)
        # m[i][i] = 0
    rel_dict = defaultdict(list)
    # costruisce la lista degli archi
    rel_list = TagTag.objects.all()
    links = []
    for rel in rel_list:
        try:
            source = tag_dict[rel.from_tag.id]
            target = tag_dict[rel.to_tag.id]
            link = { 'source': source, 'target': target, 'value': 1,}
            links.append(link)
            rel_dict[source].append(target)
            # rel_dict[target].append(source)
            print (link)
        except:
            pass
    # print rel_dict
    # calcola la matrice di dissimilarità basata sulle distanze tra tag
    max_d = 0
    for n1 in node_indexes:
        for n2 in node_indexes[n1:]:
            d = node_distance(n1, n2, rel_dict, m, [])
            m[n1][n2] = d
            m[n2][n1] = d
            max_d = max(d, max_d)
    print (m)
    # assegna posizioni ai tag più importanti
    for p in range(len(fixed_points)):
        x, y = points[p]
        node = nodes[p]
        node['x'] = x
        node['y'] = y
    # assegna posizioni agli altri tag
    for n1 in node_indexes[n_fixed:]:
        ww = 0
        xx = 0
        yy = 0
        for n2 in node_indexes:
            d = m[n1][n2]
            if d < max_distance:
                try:
                    p = points[n2]
                    w = max_d-d+1
                    xx += p[0]*w
                    yy += p[1]*w
                    ww += w
                except:
                    pass
        if ww:
            node = nodes[n1]
            node['x'] = int(xx/ww)
            node['y'] = int(yy/ww)
    print (nodes)
    tag_dict = { 'nodes': nodes, 'links': links, }
    resp = simplejson.dumps(tag_dict)
    return HttpResponse(resp, content_type='application/json')

def node_distance(n1, n2, rel_dict, m, found):
    if n1 == n2:
        return 0
    targets = rel_dict[n1]
    if not targets:
        return max_distance
    if n2 in targets:
        return 1
    distances = []
    for n in targets:
        if not n in found:
            d = m[n][n2]
            if d == max_distance:
                d = 1 + node_distance(n, n2, rel_dict, m, found+[n])
            if d < max_distance:
                m[n][n2] = d
                distances.append(d)
    if distances:
        return min(distances)
    return max_distance

def tagcloud(request):
    return render(request, 'tagcloud.html', {} )

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
"""
MMR 20180517
# inizialmente copiata da https://github.com/pgcd/asphalto3/blob/master/donations/views.py
# poi rifatta
def donate(request):
    flatpage = FlatPage.objects.get(pk=6)
    text_body = flatpage.content
    # What you want the button to do.
    language = RequestContext(request).get('LANGUAGE_CODE', 'en')
    if language.startswith('it'):
        full_lc = 'it_IT'
    else:
        full_lc = 'en_US'
    if 'username' in request.GET:
        item_name = "Donazione a RomaPaese da parte di: %s" % request.GET.get('username')
    else:
        item_name = "Donazione a RomaPaese"
    site_url = request.META["HTTP_HOST"]
    # print site_url
    paypal_dict = {
        "text_body": text_body,
        "business": "toffoli@linkroma.it",
        "item_name": item_name,
        "currency_code": "EUR",
        "amount": "25.00",
        "lc": language.upper(),
        "return": "http://%s/donate/thanks" % site_url,
        "cancel_return": "http://%s/donate" % site_url,
        "notify_url": "http://%s/donate/PayPal_IPN" % site_url,
        "btn_source": "https://www.paypal.com/%s/i/btn/btn_donate_LG.gif" % full_lc,
        "btn_alt": _("PayPal - The safer, easier way to pay online!"),
        "img_source": "https://www.paypal.com/%s/i/scr/pixel.gif" % full_lc,
        }
    return render(request, "roma/donate.html", paypal_dict)

# corrisponde al return address dell'interfaccia PayPal
def donate_thanks(request):
    return render(request, "roma/donate_thanks.html")
"""
from pois.views import zone_index_map
# from pois.models import resources_by_theme, resources_by_topo
from pois.models import resources_by_theme_count, resources_by_topo_count
from pois.models import zone_prefix_dict

def home_data(request, fv=False):
    #zone_dict = zone_index_map(request, zonetype_id=0, render_view=False)
    language = translation.get_language() or 'en'
    cache = caches['custom']
    key = 'homebody_' + language
    if request.GET.get('nocache', None) or fv:
        data_dict = None
    else:
        data_dict = cache.get(key, None)
    if not data_dict:
        print ('cache invalid')
        data_dict = {}
        summary = FlatPage.objects.get(url='/project/summary/').content
        data_dict['summary'] = summary
        """
        news = FlatPage.objects.get(url='/project/news/').content
        data_dict['news'] = news
        """
        by_theme_list = []
        themes = Tag.objects.all().order_by('weight')
        for theme in themes:
            n = resources_by_theme_count(theme)
            if n:
                by_theme_list.append([theme.id,theme.name, theme.slug, n])
        data_dict['by_theme_list'] = by_theme_list
        by_zone_list = []
        by_prov_list = []
        for zone_prefix in ['R', 'Q', 'S', 'Z']:
            topotype_name_plural = zone_prefix_dict[zone_prefix][2]
            zones = Zone.objects.filter(zonetype_id=TOPOZONE, code__istartswith=zone_prefix).order_by('name')
            topotype_sublist = []
            for zone in zones:
                n = resources_by_topo_count(zone)
                if n:
                    topotype_sublist.append([zone.code, zone.name, zone.slug, n])
            by_zone_list.append([topotype_name_plural, topotype_sublist])
        data_dict['by_zone_list'] = by_zone_list
        zones = Zone.objects.filter(zonetype_id=MACROZONE, code__istartswith='PR').order_by('name')
        for zone in zones:
            subzones = zone.zones.filter(zonetype_id=MUNICIPIO)
            zone_ids = [subzone.id for subzone in subzones]
            n = Poi.objects.select_related().filter(zones__in=zone_ids, state=1).count()
            if n:
                by_prov_list.append([zone.code, zone.name, zone.slug, n])
        data_dict['by_prov_list'] = by_prov_list
        poitypes_spotlight = Confighome.objects.exclude(poitype__isnull=True).filter(view=True).order_by('order')
        data_dict['poitypes_spotlight'] = poitypes_spotlight
        """
        site_url = request.META["HTTP_HOST"]
        d = feedparser.parse('http://%s/feed' % site_url)
        feed = d.entries and d or []
        data_dict['feed'] = feed
        """
        if not fv:
            cache.set(key, data_dict)
    #data_dict.update(zone_dict)
    return data_dict

def home(request):
    data_dict = home_data(request)
    """
    poitype_list = Poitype.objects.filter(slug__in=['caf','secondarie-superiori'])
    pois_list = Poi.objects.filter(id__in=[1819, 6039, 2202])
    data_dict['poitype_list']=poitype_list
    pois_dict_list=[poi.make_dict() for poi in pois_list]
    data_dict['pois_list']=pois_dict_list
    """
    return render(request, 'roma/home.html', data_dict )
    
def test(request):
    return render(request, 'roma/test.html', {})

from allauth.account.views import SignupView as allauthSignupView
from .forms import SignupForm
# GT 131015

class SignupView(allauthSignupView):
    form_class = SignupForm

signup = SignupView.as_view()

#180417 MMR
"""
def contactsView(request):
    flatpage = FlatPage.objects.get(url='/project/contacts/')
    text_body = flatpage.content
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['from_name']
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            text_message = "Da %s (%s)\n\n%s\n\n---------------\nEmail inviata dal sito di %s (https://%s)" % (name, from_email, message, SITE_NAME, request.META.get('HTTP_HOST', ONLINE_DOMAIN))
            try:
                email = EmailMessage(subject, text_message, SERVER_EMAIL,
                [SERVER_EMAIL,], headers = {'Reply-To': from_email})
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render (request, "roma/contacts.html", {'success': True, 'text_body': text_body, 'name': name, 'message': message})
        else:
            return render(request, 'roma/contacts.html', {'success': False, 'form': form, 'text_body': text_body, 'name': '', 'message': ''})
    else:
        form=ContactForm()
    return render(request, "roma/contacts.html", {'success': False, 'form': form, 'text_body': text_body, 'name': '', 'message': ''})
"""
def contactsView(request):
    flatpage = FlatPage.objects.get(url='/project/contacts/')
    text_body = flatpage.content
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            recaptcha = request.POST.get('g-recaptcha-response')
            data = {
                'secret': GOOGLE_RECAPTCHA_SKEY,
                'response': recaptcha
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                name = form.cleaned_data['from_name']
                from_email = form.cleaned_data['from_email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                text_message = "Da %s (%s)\n\n%s\n\n---------------\nEmail inviata dal sito di %s (https://%s)" % (name, from_email, message, SITE_NAME, request.META.get('HTTP_HOST', ONLINE_DOMAIN))
                try:
                    email = EmailMessage(subject, text_message, SERVER_EMAIL,
                    [SERVER_EMAIL,], headers = {'Reply-To': from_email})
                    email.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return render (request, "roma/contacts.html", {'success': True, 'text_body': text_body, 'name': name, 'message': message})
            else:
                nocaptcha = _('Invalid reCAPTCHA. Please try again.')
                return render(request, 'roma/contacts.html', {'success': False, 'form': form, 'text_body': text_body, 'name': '', 'message': '','nocaptcha': nocaptcha})
        else:
            return render(request, 'roma/contacts.html', {'success': False, 'form': form, 'text_body': text_body, 'name': '', 'message': '', 'nocaptcha': ''})
    else:
        form=ContactForm()
    return render(request, "roma/contacts.html", {'success': False, 'form': form, 'text_body': text_body, 'name': '', 'message': '','nocaptcha': ''})