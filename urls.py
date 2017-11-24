from __future__ import unicode_literals

# from django.conf.urls.defaults import patterns, include, url
# MMR old version - from django.conf.urls import patterns, include, url

from django.conf.urls import include, url
#MMR added
from pois.views import StreetAutocomplete, ZoneAutocomplete, PoiAutocomplete, TagAutocomplete, RouteAutocomplete, UserAutocomplete
from roma import views as roma_views
from pois import views as pois_views
from pois import search_indexes as pois_searchindexes

"""
from roma import settings
from roma.fairvillage.api import get_components, server_version, search_keys, radial_search, street_search, bbox_search, zone_search, get_pois
"""
import fairvillage
from fairvillage.api import get_components, server_version, search_keys, radial_search, street_search, bbox_search, zone_search
from fairvillage.api import get_pois, add_poi

from django.views.generic import TemplateView
from django.conf import settings

# Add before admin.autodiscover() and any form import for that matter:
"""
import autocomplete_light
autocomplete_light.autodiscover()
"""
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib.gis import admin
admin.autodiscover()

# from filebrowser.sites import site
from roma.models import Newsfeed

# from pois.views import street_autocomplete

# Routers provide an easy way of automatically determining the URL conf.
from fairvillage.api import fv_router


urlpatterns = [
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest/', include(fv_router.urls)),
    url(r'^api/', include(fv_router.urls)),
    url(r'^rest/get_components/$', get_components),
    url(r'^rest/search_keys/$', search_keys),
    url(r'^server_version/$', server_version),
    url(r'^search_keys/$', search_keys),
    url(r'^rest/radial_search/$', radial_search),
    url(r'^radial_search/$', radial_search),
    url(r'^rest/bbox_search/$', bbox_search),
    url(r'^bbox_search/$', bbox_search),
    url(r'^rest/get_pois/$', get_pois),
    url(r'^get_pois/$', get_pois),
    url(r'^zone_search/$', zone_search),
    url(r'^street_search/$', street_search),
    url(r'^add_poi/$', add_poi),

    # urlpatterns = patterns('',
    url(r'^fairvillage/$', roma_views.fairvillage, name='fairvillage'),
    url(r'^slim$', roma_views.slim, name='slim'),
    url(r'^search$', roma_views.search, name='search'),
    url(r'^tags', roma_views.tags, name='tags'),
    url(r'^tagcloud', roma_views.tagcloud, name='tagcloud'),
    url(r'^zonenet', pois_views.zone_net, name='zonenet'),
    url(r'^zonecloud', pois_views.zone_cloud, name='zonecloud'),
    url(r'^livesearch', roma_views.livesearch, name='livesearch'),
    #url(r'^type/(?P<typ>\d+)/id/(?P<obj>\d+)/$', 'roma.views.generic'),
    # url(r'^navigation_autocomplete$', pois_views.navigation_autocomplete, name='navigation_autocomplete'),
    # url(r'^cerca/(?P<q>.*)/$', pois.views.search_all', name='search_all'),
    # url(r'^cerca/', 'pois_views.search_all', name='search_all'),
    url(r'^feed', Newsfeed(),),

    # MMR 20130422
    # url(r'^$', TemplateView.as_view(template_name='roma/index.html'), name='index',),
    # url(r'^$', 'pois.views.zone_index_map', {'zonetype_id': 0}, name='macrozone'),
    url(r'^$', roma_views.home, name='home'),
    url(r'^robots.txt$', roma_views.robots, name='robots'),
    url(r'^test$', roma_views.test, name='test'),
    url(r'^home$', roma_views.home, name='home',),
    # url(r'^about$', TemplateView.as_view(template_name='roma/about.html'), name='about',),
    url(r'^poitypes$', TemplateView.as_view(template_name='pois/poitype_index.html'), name='poitypes',),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Import urls from app autocomplete_light
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # Import urls from app datatrans
    url(r'^datatrans/', include('datatrans.urls')),

    # Import urls from app pois
    # MMR 20130422 - aggiunto namespace
    # url(r'^pois/', include('pois.urls')),
    url(r'^pois/', include('pois.urls', namespace='pois')),

    # Import urls from app autocomplete_light
    # MMR - url(r'autocomplete/', include('autocomplete_light.urls')),

    url(r'^la-mia-zona', pois_views.choose_zone),
    url(r'^macrozone', pois_views.zone_index_map, {'zonetype_id': 0, 'prefix': 'RM.'}, name='macrozone'),
    url(r'^province', pois_views.zone_index_map, {'zonetype_id': 0, 'prefix': 'PR.'}, name='province'),
    url(r'^municipi$', pois_views.zone_index_map, {'zonetype_id': 7, 'prefix': 'M.'}, name='municipi'),
    url(r'^comuni', pois_views.zone_index_map, {'zonetype_id': 7, 'prefix': 'COM.'}, name='comuni'),
    url(r'^vecchi_municipi$', pois_views.zone_index_map, {'zonetype_id': 1}, name='vecchi municipi'),
    # url(r'^zone$', pois_views.zone_index_map, {'zonetype_id': 2}),
    url(r'^topo$', pois_views.zone_index_map, {'zonetype_id': 3}),
    url(r'^rioni$', pois_views.zone_index_map, {'zonetype_id': 3, 'prefix': 'R.'}),
    url(r'^quartieri$', pois_views.zone_index_map, {'zonetype_id': 3, 'prefix': 'Q.'}),
    url(r'^suburbi$', pois_views.zone_index_map, {'zonetype_id': 3, 'prefix': 'S.'}),
    url(r'^agro-romano$', pois_views.zone_index_map, {'zonetype_id': 3, 'prefix': 'Z.'}),
    url(r'^ville$', pois_views.zone_index_map, {'zonetype_id': 4}),
    url(r'^parchi$', pois_views.zone_index_map, {'zonetype_id': 5}),
    url(r'^cap$', pois_views.zone_index_map, {'zonetype_id': 6}),
    url(r'^itinerari$', pois_views.route_index),
    url(r'^muoviroma$', pois_views.muoviroma),

    url(r'^tipi-di-zona$', pois_views.zonetype_index),
    url(r'^tipo-di-zona/(?P<zonetype_slug>.+)/$', pois_views.zonetype_detail_by_slug),
    url(r'^aree-tematiche$', pois_views.tag_index),
    url(r'^categorie-di-risorsa$', pois_views.category_index), # poitype_index
    url(r'^reti-di-risorse$', pois_views.resource_networks),
    url(r'^mappe-di-risorse$', pois_views.resource_maps),

    # url(r'^tag/(?P<tag_name>\w*)/$', 'roma.views.set_tag'),
    url(r'^tag_toggle/(?P<tag_id>\d+)/$', pois_views.tag_toggle),
    url(r'^tag_set/(?P<tag_id>\d+)/$', pois_views.tag_set),
    url(r'^zone_themes/$', pois_views.zone_themes),
    url(r'^zone_toggle_theme/(?P<tag_id>\d+)/$', pois_views.zone_toggle_theme),
    url(r'^zone_set_theme/(?P<tag_id>\d+)/$', pois_views.zone_set_theme),
    url(r'^zone_set_category/(?P<klass>\d+)/$', pois_views.zone_set_category),

    # Import urls from app flatpages
    # url(r'^', include('django.contrib.flatpages.urls')),

    url(r'^macrozona/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='macrozona'),
    url(r'^municipio/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='municipio'),
    url(r'^ex-municipio/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='ex-municipio'),
    url(r'^zona-urbanistica/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='zona-urbanistica'),
    url(r'^zona-toponomastica/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='zona-toponomastica'),
    url(r'^rione/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='rione'),
    url(r'^quartiere/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='quartiere'),
    url(r'^suburbio/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='suburbio'),
    url(r'^mappa-zona/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='mappa-zona'),
    url(r'^indice-zona/(?P<zone_slug>.+)/$', pois_views.zone_tag_index_by_slug, name='zona-tema'),
    url(r'^zona-cap/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='zona-cap'),
    url(r'^area-protetta/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='area-protetta'),
    url(r'^villa-storica/(?P<zone_slug>.+)/$', pois_views.zone_map_by_slug, name='villa-storica'),
    url(r'^zona/(?P<zone_slug>.+)/$', pois_views.zone_detail_by_slug, name='zona'),
    url(r'^itinerario/(?P<route_slug>.+)/$', pois_views.route_detail_by_slug, name='itinerario'),
    url(r'^toponimo/(?P<street_slug>.+)/$', pois_views.street_detail_by_slug, name='toponimo'),
    url(r'^viewport$', pois_views.viewport, name='refresh viewport'),
    url(r'^tema/(?P<tag_slug>[\w-]+)/zona/(?P<zone_slug>.+)/$', pois_views.tag_zone_detail_by_slug, name='tema-zona'),
    url(r'^tema/(?P<tag_slug>.+)/$', pois_views.tag_detail_by_slug, name='tema'),
    url(r'^categoria/(?P<klass_slug>[\w-]+)/zona/(?P<zone_slug>.+)/$', pois_views.poitype_zone_detail_by_slugs, name='categoria-zona'),
    url(r'^categoria/(?P<klass_slug>[\w-]+)/tema/(?P<tag_slug>.+)/$', pois_views.poitype_tag_detail_by_slugs, name='categoria-tema'),
    url(r'^categoria/(?P<klass_slug>.+)/$', pois_views.poitype_detail_by_slug, name='categoria'),
    url(r'^rete/(?P<poi_slug>[\w-]+)/zona/(?P<zone_slug>.+)/$', pois_views.poi_network_zone_by_slug, name='rete-zona'),
    url(r'^rete/(?P<poi_slug>[\w-]+)/$', pois_views.poi_network_by_slug, name='rete'),
    url(r'^risorsa/(?P<poi_slug>[\w-]+)/rete/$', pois_views.poi_network_by_slug, name='risorsa-rete'),
    url(r'^risorsa/(?P<poi_slug>[\w-]+)/mappa/$', pois_views.resource_map_by_slug, name='risorsa-mappa'),
    url(r'^risorsa/(?P<poi_slug>.+)/$', pois_views.poi_detail_by_slug, name='risorsa'),
    url(r'^nuova-risorsa$', pois_views.poi_new),
    url(r'^nuova-risorsa/(?P<poi_id>.+)/$', pois_views.poi_view),
    url(r'^annota-risorsa/(?P<poi_slug>.+)/$', pois_views.poi_add_note_by_slug, name='feedback'),
    url(r'^risorse-recenti$', pois_views.pois_recent, name='risorse recenti'),
    url(r'^risorse-aggiornate$', pois_views.pois_updates, name='risorse aggiornate'),
    url(r'^poi-contributors$', pois_views.poi_contributors, name='contributors'),
    url(r'^donate$', roma_views.donate, name='donazione'),
    url(r'^donate/thanks$', roma_views.donate_thanks, name='ringraziamento donazione'),
    # url(r'^donate/PayPal_IPN', 'roma.views.donate_notify, name='notifica donazione'),
    url(r'^my_resources/$', pois_views.my_resources),
    url(r'^set_viewport$', pois_views.set_viewport, name='set viewport'),
    url(r'^viewport_pois$', pois_views.viewport_pois, name='risorse in viewport'),
    url(r'^update_colocations$', pois_views.pois_update_colocations, name='pois_update_colocations'),
    url(r'^analisi-risorse$', pois_views.poi_analysis, name='poi_analysis'),
    
    url(r'^toponimo-autocomplete/$', StreetAutocomplete.as_view(),name='toponimo-autocomplete'),
    url(r'^zona-autocomplete/$', ZoneAutocomplete.as_view(),name='zona-autocomplete'),
    url(r'^risorsa-autocomplete/$', PoiAutocomplete.as_view(),name='risorsa-autocomplete'),
    url(r'^tema-autocomplete/$', TagAutocomplete.as_view(),name='tema-autocomplete'),
    url(r'^itinerario-autocomplete/$', RouteAutocomplete.as_view(),name='itinerario-autocomplete'),
    url(r'^utente-autocomplete/$', UserAutocomplete.as_view(),name='utente-autocomplete'),
    url(r'^navigation_autocomplete$', pois_searchindexes.navigation_autocomplete, name='navigation_autocomplete'),
    url(r'^cerca/', pois_views.search_all, name='search_all'),
]
"""
urlpatterns += patterns('',
    url (r'^/rmppstdipn/', include('paypal.standard.ipn.urls')),
)   
"""
# MMR old version - urlpatterns += patterns('',
urlpatterns += [
    url (r'^accounts/signup/$', roma_views.signup, name='account_signup'), # 131015 GT
    url (r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/', TemplateView.as_view(template_name='account/profile.html'), name='welcome',),
]   

"""
MMR temporaneamente disattivato
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
"""
from django.views import static as django_views_static
# MMMR old version - urlpatterns += patterns('',
urlpatterns += [
    # url(r'^blog$', 'pois.views.blogs_index'),
    # url(r'^blog/(?P<blog_slug>.+)/$', 'pois.views.blog_detail_by_slug'),
    # url(r'^blog/(?P<blog_slug>.+)/posts$', 'pois.views.blog_posts_by_slug'),
    # url(r'^edit-blog/(?P<blog_slug>.+)$', 'pois.views.blog_edit'),
    # url(r'^save-blog$', 'pois.views.blog_save'),
    # url(r'^new-post/(?P<blog_slug>.+)$', 'pois.views.post_new'),
    # url(r'^edit-post/(?P<post_slug>.+)$', 'pois.views.post_edit'),
    # url(r'^save-post$', 'pois.views.post_save'),
    # url(r'^add/tags/?$', 'pois.views.newTag'), 

    # richtext_blog definitions
    # url(r'', include('richtext_blog.urls')),
    # MMR url(r'blogs/', include('richtext_blog.urls')),
    # 3rd party url definitions
    url(r'^tinymce/', include('tinymce.urls')),
    # MMR - url(r'^admin/filebrowser/', include(site.urls)),
    # MMR - url(r'^grappelli/', include('grappelli.urls')),
    url(r'^captcha/', include('captcha.urls')),
    # Media
    url(r'^media/(?P<path>.*)$', django_views_static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    #MMR old version - urlpatterns += patterns('',
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
if settings.USE_LOCALEURL:
    #MMR old version - urlpatterns += patterns('',
    urlpatterns += [
        url(r'^localeurl/', include('localeurl.urls')),
    ]

if settings.USE_HAYSTACK:
    # urlpatterns += patterns('', url(r'^haystack/', include('haystack.urls')),
    from haystack.views import SearchView
    # from haystack.forms import ModelSearchForm
    from pois.search_indexes import poisModelSearchForm
    from haystack.query import SearchQuerySet
    sqs = SearchQuerySet()
    # MMR old version - urlpatterns += patterns('haystack.views',
    urlpatterns += [
        url(r'^cercaveloce/', SearchView(
                template='search/search.html',
                searchqueryset=sqs,
                form_class=poisModelSearchForm,
                results_per_page=100,
                load_all=False
            ), name='haystack_search'),
    ]
