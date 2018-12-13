from django import forms
from useraction.models import *

class ruleform(forms.Form):
    rulename=forms.CharField()

class commform(forms.ModelForm):
    class Meta:
        model=commands
        exclude = ['id','cuser','rulename']

    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in dict(cls.base_fields).items():
            field_obj.widget.attrs['class'] = 'form-control'
        return forms.ModelForm.__new__(cls)
            # field_obj.widget.attrs.update({'class':"form-control"})