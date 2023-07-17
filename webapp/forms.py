from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'cost', 'stock', 'image']
        widgets = {
            "description": widgets.Textarea(attrs={"cols": 30, "rows": 5, "class": "test"}),

        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label="Поиск")
