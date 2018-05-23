from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pois.models import Poi, Poitype, Tag, Zone, PoiZone
from pois.views import resources_by_category_and_zone

class PoiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Poi.objects.filter(state=1).order_by('name')

    def location (self, obj):
        return '/risorsa/%s' % obj.slug
        
    def lastmod(self, obj):
        return obj.modified

class PoitypeSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        poi_list = Poi.objects.filter(state=1)
        poitype_ids = poi_list.values_list('poitype_id', flat=True).distinct()
        return Poitype.objects.filter(klass__in=poitype_ids)

    def location (self, obj):
        return '/categoria/%s' % obj.slug
        
    def lastmod(self, obj):
        return obj.modified

class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Tag.objects.all().exclude(id=49)

    def location (self, obj):
        return '/tema/%s' % obj.slug
        
    def lastmod(self, obj):
        return obj.modified
        
class PoitypeZone(object):
    slugs = []
    
    def __init__(self, slugs=None):
        if slugs is None:
            slugs = []
        self.data = slugs

def make_PoitypeZone(slugs):
    return PoitypeZone(slugs)
    
class PoitypeZoneSitemap (Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poi_list = Poi.objects.filter(state=1).order_by('poitype_id')
        poitype_ids = poi_list.values_list('poitype_id', flat=True).distinct()
        poitypes = Poitype.objects.filter(klass__in=poitype_ids)
        poizones = PoiZone.objects.all().order_by('zone_id')
        poizones_ids = poizones.values_list('zone_id', flat=True).distinct()
        zones = Zone.objects.filter(zonetype_id__in=(0,3,7),pk__in=poizones_ids)
        poitypezone = []
        for zone in zones:
            for poitype in poitypes:
                poi_list = resources_by_category_and_zone(poitype.klass, zone, select_related=True)
                if poi_list:
                    poitypezone.append(make_PoitypeZone([poitype.slug,zone.slug,]))       
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['/nuova-risorsa', '/promuovere-attivita-roma-lazio/', '/about-us/', '/contattare-redazione-romapaese']

    def location(self, item):
        return item

class Section(object):
    name = ""

    def __init__(self, name):
        self.name = name

def make_section(name):
    section = Section(name)
    return section
    
all_sitemaps = {}
section = make_section('risorse')
sitemap = PoiSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categorie')
sitemap = PoitypeSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('temi')
sitemap = TagSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categoriazona')
sitemap = PoitypeZoneSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('static')
sitemap = StaticSitemap()
all_sitemaps[section.name] = sitemap
