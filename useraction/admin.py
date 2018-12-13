from django.contrib import admin
from .models import *
# Register your models here.
class ruleAdmin(admin.ModelAdmin):
    list_display = ('rulename',)
    # exclude = ['node_signer']
    def save_model(self, request, obj, form, change):
        obj.cuser = str(request.user)
        obj.save()
class commAdmin(admin.ModelAdmin):
    list_display = ('rulename','zhiling',)
    def save_model(self, request, obj, form, change):
        obj.cuser = str(request.user)
        obj.save()

class persomAdmin(admin.ModelAdmin):
    list_display = ('descname','nickname')
    exclude = []
    # pass
class qunAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = []
class qunperadmin(admin.ModelAdmin):
    list_display = ('qunname',)
    filter_horizontal = ("qunrulename",)
    exclude = []
class perperadmin(admin.ModelAdmin):
    list_display = ('Sinname',)
    filter_horizontal = ("qunrulename",)
    exclude = []
admin.site.register(rulelistmodel,ruleAdmin)
admin.site.register(commands,commAdmin)
admin.site.register(person,persomAdmin)
admin.site.register(qun,qunAdmin)
admin.site.register(QunPer,qunperadmin)
admin.site.register(SinPer,perperadmin)