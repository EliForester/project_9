from django import forms
from django.forms.widgets import SelectDateWidget

from .models import Menu


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)
        widgets = {'expiration_date': SelectDateWidget(
            years=range(2000, 2051))}
