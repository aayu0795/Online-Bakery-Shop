from django import forms
from items.models import Category, Item


class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class Item_form(forms.ModelForm):
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'rows': 2
    }))

    class Meta:
        model = Item
        fields = "__all__"
