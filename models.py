# MMR old vesrion -import HTMLParser
from __future__ import unicode_literals
# from django.utils.encoding import python_2_unicode_compatible
import six
from six import python_2_unicode_compatible

from html.parser import HTMLParser
from django.db import models
# from django.contrib import adminindexable_models

from django.contrib.auth.models import Group
from django.contrib.syndication.views import Feed

# from cuser.middleware import CuserMiddleware
from pois.models import Zone, Odonym, Poi # MMR temporaneamente disattivato -, Blog
indexable_models = [Zone, Odonym, Poi]


class Newsfeed(Feed):
    title = "RomaPaese"
    #MMR temoraneamente disattivato - link = "/blog/notizie-da-romapaese/"
    description = "Notizie ed eventi"
    
    """
    MMR temporaneamente disattivato
    def items(self):
        # return Post.objects.order_by('-created')[:5]
        slug = self.link.split('/')[2]
        blog = Blog.objects.get(slug=slug)
        return blog.posts().order_by('-created')[:5]
    """
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        text = item.content
        html_parser = HTMLParser.HTMLParser()
        text = html_parser.unescape(text)
        return text

    def item_link(self, item):
        return item.get_absolute_url()

"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import connection
from django.db.models import signals

def zone_get_indexable_fields (self):
    return ('name', 'code', 'description')
Zone.get_indexable_fields = zone_get_indexable_fields
def street_get_indexable_fields (self):
    return ('name',)
Odonym.get_indexable_fields = street_get_indexable_fields
def poi_get_indexable_fields (self):
    return ('name', 'description')
Poi.get_indexable_fields = poi_get_indexable_fields

# from http://www.djangosnippets.org/snippets/1328/
class VectorField (models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['editable'] = False
        kwargs['serialize'] = False
        super(VectorField, self).__init__(*args, **kwargs)

    # def db_type( self ):
    # http://stackoverflow.com/questions/10216019/django-syncdb-error-after-updating-to-1-4
    def db_type (self, connection):
        return 'tsvector'

class Search(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey()
    title = models.CharField(max_length=100, blank=True, null=True)
    # url = models.CharField(max_length=20, blank=True, null=True)
    index = VectorField()

    @staticmethod
    def query(search_text):
        if search_text and len(search_text)>1:
            search_text += ':*' 
        results = Search.objects.extra(where=["index @@ to_tsquery(%s)"], params=[search_text,])
        print search_text
        # print results
        return results

# bits from http://www.arnebrodowski.de/blog/add-full-text-search-to-your-django-project-with-whoosh.html
def update_index(instance):
    # catalog = 'pg_catalog.english'
    catalog = 'pg_catalog.italian'
    field_names = instance.get_indexable_fields()
    # title = str(getattr(instance, field_names[0]))
    title = getattr(instance, field_names[0])
    data = [title]
    for f in field_names[1:]:
        val = getattr(instance, f)
        if val:
            # data.append(str(val))
            data.append(val)
    data = " ".join(data)
    
    content_type = ContentType.objects.get_for_model(instance)
    try:
        search = Search.objects.get(content_type__pk=content_type.id, object_id=instance.id)
    except Search.DoesNotExist:
        search = Search.objects.create(content_object=instance)
        search.save()

    cursor = connection.cursor()
    sql = "update roma_search set index = to_tsvector(%s, %s), title = %s where id = %s"
    cursor.execute(sql, (catalog, data, title, search.id))
    cursor.execute("COMMIT;")
    cursor.close()

def on_saved(sender, instance, created, **kwargs):
    if hasattr(instance, "get_indexable_fields"):
        update_index(instance)

def remove_from_fulltext_index(sender, instance, *args, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)
    try:
        search = Search.objects.get(content_type__pk=content_type.id, object_id=instance.id)
        search.delete()
    except Search.DoesNotExist:
        pass
    except:
        pass

def clear_fulltext_index():
    Search.objects.all().delete()

def rebuild_fulltext_index():
    clear_fulltext_index()
    for model in indexable_models:
        instances = model.objects.all()
        for instance in instances:
            if model == Odonym:
                if not instance.get_pois():
                    continue
            # update_index(None, instance, created=True)
            update_index(instance)

# signals.post_save.connect(update_index)
signals.post_save.connect(on_saved)
signals.pre_delete.connect(remove_from_fulltext_index)
"""

# form https://github.com/pgcd/asphalto3/blob/master/donations/models.py
@python_2_unicode_compatible
class Donation(models.Model):
    from_email = models.EmailField(blank=True) # payer_email
    from_username = models.CharField(max_length=255, blank=True) # custom
    amount = models.FloatField(blank=True, default=0)
    status = models.CharField(max_length=50, blank=True)
    memo = models.TextField(blank=True)

    def __str__(self):
        return u"%s: %s" % (self.amount, self.from_email)

"""
from paypal.standard.ipn.signals import payment_was_successful

# from https://github.com/pgcd/asphalto3/blob/master/donations/models.py
def donation_successful(sender, **kwargs):
    ""
    @param sender: PayPalStandardBase
    @param kwargs:
    ""
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    username = ipn_obj.custom or ipn_obj.item_name.replace("Donazione da parte di: ", '')
    d, created = Donation.objects.get_or_create(from_email=ipn_obj.payer_email,
                                                from_username=username,
                                                amount=ipn_obj.auth_amount,
                                                memo=ipn_obj.memo)

    d.status=ipn_obj.auth_status
    d.save()

payment_was_successful.connect(donation_successful)
"""

from datatrans.utils import register
from django.contrib.flatpages.models import FlatPage

class FlatPageTranslation(object):
    fields = ('content')
register(FlatPage, FlatPageTranslation)

"""
class PoiTranslation(object):
    fields = ('short', 'description')
register(Poi, PoiTranslation)
"""

def on_email_confirmed(*args, **kwargs):
    user = kwargs['email_address'].user
    group_verified = Group.objects.get(name='verified')
    group_verified.user_set.add(user)

from allauth.account.signals import email_confirmed
email_confirmed.connect(on_email_confirmed)
