from .models import Fence
from django_select2 import forms as s2forms
from django import forms


class FenceWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'marking_icontains',
    ]


class FencingForm(forms.ModelForm):

    class Meta:
        model = Fence
        fields = ['marking']

        widgets = {'fence': FenceWidget}
