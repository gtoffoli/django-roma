from django.db.models import Q
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pois.models import Poi, Poitype, Tag, Zone, PoiZone

class PoiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Poi.objects.filter(state=1).order_by('name')

    def location (self, obj):
        return '/risorsa/%s/' % obj.slug
        
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
        return '/categoria/%s/' % obj.slug
        
    def lastmod(self, obj):
        return obj.modified

class TagSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Tag.objects.all().exclude(id=49)

    def location (self, obj):
        return '/tema/%s/' % obj.slug
        
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

def poitypes_with_resources():
    poi_list = Poi.objects.filter(state=1).order_by('poitype_id')
    poitype_ids = poi_list.values_list('poitype_id', flat=True).distinct()
    poitypes = Poitype.objects.filter(klass__in=poitype_ids)
    return poitypes

def zones_with_resources():
    zone_list = PoiZone.objects.filter(poi__state=1).order_by('zone_id')
    zone_ids = zone_list.values_list('zone_id', flat=True).distinct()
    zones = Zone.objects.filter(pk__in=zone_ids)
    return zones

def make_poitypeszone(zones, poitypes):
    poitypezone = []
    for zone in zones:
        q = Q(zones=zone)
        for poitype in poitypes:
            poi_list = Poi.objects.filter(q & Q(poitype_id=poitype.klass, state=1))
            if poi_list:
                poitypezone.append(make_PoitypeZone([poitype.slug,zone.slug,]))
    return poitypezone
    
class PoitypeMacrozoneSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones = Zone.objects.filter(zonetype_id = 0).exclude(code='ROMA')
        poitypezone = []
        for zone in zones:
            subzones = zone.zones.filter(zonetype_id=7)
            zone_ids = [subzone.id for subzone in subzones]
            q = Q(zones__in=zone_ids)
            for poitype in poitypes:
                poi_list = Poi.objects.filter(q & Q(poitype_id=poitype.klass, state=1))
                if poi_list:
                    poitypezone.append(make_PoitypeZone([poitype.slug,zone.slug,]))       
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeMunicipiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 7, code__startswith='M.')
        poitypezone = make_poitypeszone(zones, poitypes)
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeQuartieriSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 3, code__startswith='Q.')
        poitypezone = make_poitypeszone(zones, poitypes)     
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeRioniSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 3, code__startswith='R.')
        poitypezone = make_poitypeszone(zones, poitypes)
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeSuburbiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 3, code__startswith='S.')
        poitypezone = make_poitypeszone(zones, poitypes)
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeAgroromanoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 3, code__startswith='Z.')
        poitypezone = []
        poitypezone = make_poitypeszone(zones, poitypes)
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])

class PoitypeComuniSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poitypes = poitypes_with_resources()
        zones_ids = zones_with_resources()
        zones = Zone.objects.filter(pk__in=zones_ids, zonetype_id = 7, code__startswith='COM.')
        poitypezone = make_poitypeszone(zones, poitypes)
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])
        
"""
class PoitypeMunicipiSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"
    
    def items(self):
        poi_list = Poi.objects.filter(state=1).order_by('poitype_id')
        poitype_ids = poi_list.values_list('poitype_id', flat=True).distinct()
        poitypes = Poitype.objects.filter(klass__in=poitype_ids)
        zones = Zone.objects.filter(zonetype_id__in=(0,3,7)).exclude(code='ROMA')
        poitypezone = []
        for zone in zones[:10]:
            if zone.zonetype_id == 0:
                subzones = zone.zones.filter(zonetype_id=7)
                zone_ids = [subzone.id for subzone in subzones]
                q = Q(zones__in=zone_ids)
            else:
                q = Q(zones=zone)
            for poitype in poitypes[:10]:
                poi_list = Poi.objects.filter(q & Q(poitype_id=poitype.klass, state=1))
                if poi_list:
                    poitypezone.append(make_PoitypeZone([poitype.slug,zone.slug,]))       
        return poitypezone
         
    def location (self, obj):
        return '/categoria/%s/zona/%s/' % (obj.data[0],obj.data[1])
"""
class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['/', '/nuova-risorsa', '/promuovere-attivita-roma-lazio/', '/about-us/', '/contattare-redazione-romapaese']

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

section = make_section('categoriemacrozone')
sitemap = PoitypeMacrozoneSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categoriemunicipi')
sitemap = PoitypeMunicipiSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categoriequartieri')
sitemap = PoitypeQuartieriSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categorierioni')
sitemap = PoitypeRioniSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categoriesuburbi')
sitemap = PoitypeSuburbiSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categorieagroromano')
sitemap = PoitypeAgroromanoSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('categoriecomuni')
sitemap = PoitypeComuniSitemap()
all_sitemaps[section.name] = sitemap

section = make_section('static')
sitemap = StaticSitemap()
all_sitemaps[section.name] = sitemap
