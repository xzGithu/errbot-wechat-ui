"""webui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from useraction import views
from django.conf import settings
from django.views import static
from useraction.resful import CommandList
from rest_framework import routers
from useraction.resful import CommandViewSet
router=routers.DefaultRouter()
router.register(r'commands',CommandViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'command/',CommandViewSet.as_view()),
    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
    url(r'login/', views.login, name='login'),
    url(r'logout/', views.logout, name='logout'),
    url(r'password_change/', views.password_change, name='password_change'),
    url(r'^accounts/changepwd/$', views.changepwd, name="changepwd"),
    url(r'^accounts/register/', views.registuser, name="regist"),
    url(r'hello',views.hello,name="hello"),
    url(r'^errbot/',include('errbotui.urls')),
    url(r'^permis/',include('useraction.urls')),
    url(r'^static/(?P<path>.*)',static.serve,{"document_root":settings.STATIC_ROOT}),

]
