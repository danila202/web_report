from .models import Fence
from django import forms


class FencingForm(forms.Form):

    class Meta:
        model = Fence
        fields = ['marking']

    marking = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите ограждение'}))
