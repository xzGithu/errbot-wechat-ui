from django.conf.urls import url
from errbotui.views import *
urlpatterns = [
    url(r'rulelist/(?P<table>\w+)/$',rulelist,name="rulelist"),
    url(r'fanglist/',getfang,name="fanglist"),
    url(r'newrule/(?P<fangan>.+)/$',newrule,name="newrule"),
    url(r'newcommand/(?P<fangan>\w+)/(?P<rule>\w+)/$',newcommand,name="newcommand"),
    url(r'getrule/(?P<fangan>\w+)/(?P<rule>\w+)/$',getrule,name="getrule"),
    url(r'modrule/(?P<pk>\d+)/$', modrule, name="modrule"),
    # url(r'modcomm/(?P<pk>\d+)/(?P<fangan>\w+)/(?P<rule>\w+)/$', modcomm,name="modcomm"),
    url(r'modcomm/(?P<pk>\d+)/$', modcomm, name="modcomm"),
    url(r'delcomm/(?P<pk>\d+)/$', delcomm,name="delcomm"),
    url(r'delrule/(?P<pk>\d+)/$',delrule,name="delrule"),
    url(r'alldel/',alldel,name="alldel"),
    url(r'modrenew/(?P<rulename>\w+)/$',modrenew,name="modrenew"),
    url(r'modadd/(?P<rule>\w+)/(?P<fangan>\w+)/$',modrenewcommand,name="modadd"),
    url(r'commadd/(?P<fangan>\w+)/(?P<rule>\w+)/$',commadd,name="commadd"),
    url(r'checkrule/',postrule,name="postrule"),
    url(r'queryrule/(?P<rulename>.+)',queryrule,name="queryrule"),
]