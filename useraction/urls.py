from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'qunpermis/', qunpermis, name="qunpermis"),
    url(r'perpermis/', userpermis, name="userpermis"),
    url(r'lqunper/(?P<table>\w+)/(?P<pk>\d+)/$',lqunper,name="lqunper"),
    url(r'perrulelist/(?P<type>\w+)/(?P<name>.+)/(?P<pk>\d+)/$',perrulelist,name="perrulelist"),
    url(r'confqunper',confqunper,name="confqunper"),
    url(r'qunper/(?P<name>\w+)',qunper,name="qunper"),
    url(r'removerule/(?P<type>\w+)/(?P<pk1>\d+)/(?P<pk2>\w+)',removerule,name="removerule"),
]