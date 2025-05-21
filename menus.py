from __future__ import unicode_literals

from menu import Menu, MenuItem
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

def zones_children(request):
    user = request.user
    children = []
    """
    children.append (MenuItem(
         _("My zone"),
         url='/la-mia-zona',
         weight=10,
         ))
    """
    children.append(MenuItem(_("Macrozones"),
         url='/macrozone-roma',
         weight=10,
    ))
    children.append(MenuItem(_("Municipalities"),
         url='/municipi-roma',
         weight=10,
         ))
    children.append(MenuItem(_("Historical quarters"),
         url='/rioni-roma',
         weight=10,
    ))
    children.append(MenuItem(_("Quarters"),
             url='/quartieri-roma',
             weight=10,
             ))
    children.append(MenuItem(_("Quarter extensions"),
             url='/suburbi-roma',
             weight=10,
             ))
    children.append(MenuItem(_("Suburban zones"),
             url='/zone-agro-romano',
             weight=10,
             ))
    if user.is_superuser or user.is_staff:
        children.append(MenuItem(_("Traditional city districts"),
                 url='/topo',
                 weight=10,
                 ))
    children.append(MenuItem(_("Provinces"),
         url='/province-lazio',
         weight=10,
         ))
    if (user.is_superuser or user.is_staff):
        children.append(MenuItem(_("Zipcode areas"),
             url='/cap',
             weight=80,
             ))
        children.append(MenuItem(_("Zone types"),
             url='report/tipi-di-zona',
             weight=80,
             ))
    """
    if user.is_authenticated:
        children.append(MenuItem("Muoversi a Roma",
                 url='/muoviroma',
                 weight=80,
                 ))
    """
    return children

def project_children(request):
    user = request.user
    children = []
    children.append (MenuItem(
         _("About"),
         url='/project/about',
         weight=80,
        ))
    children.append (MenuItem(
         _("Our partners"),
         url='/project/partners',
         weight=80,
        ))
    children.append (MenuItem(
         _("Help us"),
         url='/project/collaborate',
         weight=80,
        ))
    children.append (MenuItem(
         _("RomaPaese and the schools"),
         url='/project/schools',
         weight=80,
        ))
    if (user.is_superuser or user.is_staff):
        children.append (MenuItem(
            _("Donate"),
            url='/donate',
            weight=80,
            ))
    
    """
    children.append (MenuItem(
         _("Contacts"),
         url='/contatti',
         weight=80,
        ))
    """
    return children

def resources_children(request):
    user = request.user
    children = []
    children.append (MenuItem(
        _("By theme area"),
        url='/risorse-utili-roma-lazio-aree-tematiche',
        weight=80,
    ))
    children.append (MenuItem(
        _("By category"),
        url='/risorse-utili-roma-lazio-categorie',
        weight=80,
    ))
    if user.is_superuser or user.is_staff:

        children.append (MenuItem(
            _("By affiliation"),
            url='/report/reti-di-risorse',
            weight=80,
        ))
        children.append(MenuItem(
            _("Routes"),
            url='/report/itinerari',
            weight=80,
        ))
        children.append (MenuItem(
            _("Resource networks"),
            url='/report/mappe-di-risorse',
            weight=80,
        ))
        children.append (MenuItem(
            _("New entries"),
            url='/report/risorse-recenti',
            weight=80,
        ))
        children.append (MenuItem(
            _("Updates"),
            url='/report/risorse-aggiornate',
            weight=80,
        ))
        children.append (MenuItem(
            _("To be reviewed"),
            url='/report/analisi-risorse',
            weight=80,
        ))
        children.append (MenuItem(
        _("Top contributors"),
            url='/report/poi-contributors',
            weight=80,
        ))
    """
    children.append (MenuItem(
        _("Advanced search"),
        url='/cerca/',
        weight=80,
    ))
    children.append (MenuItem(
        _("How to search"),
        url='/help/search',
        weight=80,
    ))
    """
    children.append (MenuItem(
        _("Suggest a resource"),
        url='/nuova-risorsa',
        weight=80,
    ))
    children.append (MenuItem(
        _("Promote your business"),
        url='/promuovere-attivita-roma-lazio/',
        weight=80,
    ))
    return children

def community_children(request):
    children = []
    """
    children.append (MenuItem(
         _("Our blogs"),
         url='/blog',
         weight=80,
        ))
    """
    children.append (MenuItem(
         _("From the schools"),
         url='/community/schools',
         weight=80,
        ))
    children.append (MenuItem(
         _("Citizens' committees"),
         url='/community/citizens',
         weight=80,
        ))
    children.append (MenuItem(
         _("Ethnic and linguistic communities"),
         url='/community/cultures',
         weight=80,
        ))
    children.append (MenuItem(
         _("Social networks"),
         url='/community/networks',
         weight=80,
        ))
    children.append (MenuItem(
         _("Why register"),
         url='/community/why-register',
         weight=80,
        ))
    return children
    
def user_children(request):
    children = []
    if not request.user.is_authenticated:
        children.append (MenuItem(
             "Login",
             url='/accounts/login/',
             weight=80,
            ))
    if request.user.is_authenticated and request.user.is_superuser:
        children.append (MenuItem(
             "Admin",
             reverse("admin:index"),
             weight=80,
             ))
    if request.user.is_authenticated:
        children.append (MenuItem(
             "Logout",
             url='/accounts/logout/',
             weight=80,
            ))
    return children

def user_menu_title(request):
    if request.user.is_authenticated:
        user = request.user
        fullname = '%s %s' % (user.first_name, user.last_name)
        if fullname.strip():
            return fullname
        else:
            return user.username
    else:
        return 'Utente'

Menu.items = {}
Menu.sorted = {}

# Add a few items to our main menu
Menu.add_item("main", MenuItem(ugettext_lazy("The resources"),
                               url='/r',
                               weight=10,
                               children=resources_children,
                               separator=True))
Menu.add_item("main", MenuItem(ugettext_lazy("The zones"),
                               url='/z',
                               weight=20,
                               children=zones_children,
                               separator=True))
"""
180420 MMR
Menu.add_item("main", MenuItem(ugettext_lazy("The project"),
                               url='/p',
                               weight=30,
                               children=project_children,
                               separator=True))     
Menu.add_item("main", MenuItem(ugettext_lazy("Community"),
                           url='/c',
                           weight=40,
                           children=community_children,
                           separator=True))
"""
#180420 MMR
Menu.add_item("main", MenuItem(ugettext_lazy("Project"),
                           url='/about-us/',
                           weight=40,
                           separator=True))
Menu.add_item("main", MenuItem(ugettext_lazy("Privacy"),
                           url='/privacy/',
                           weight=40,
                           separator=True))
Menu.add_item("main", MenuItem(ugettext_lazy("Contacts"),
                           url='/contattare-redazione-romapaese',
                           weight=40,
                           separator=False))
