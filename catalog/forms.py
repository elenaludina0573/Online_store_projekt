from django.db.models import BooleanField
from django.forms import ModelForm, forms
from catalog.models import Product


forbidden_words = [
                   'казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at', 'owner')

    def clean_product_name(self):

        clean_data = self.cleaned_data.get['name']
        if clean_data in forbidden_words:
            raise forms.ValidationError(f'Наименование не должно содержать слова: {forbidden_words}')
        else:
            return clean_data

    def clean_product_description(self):
        clean_data = self.cleaned_data.get['description']
        if clean_data in forbidden_words:
            raise forms.ValidationError(f'Наименование не должно содержать слова: {forbidden_words}')
        else:
            return clean_data


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        fields = ['publication', 'description', 'category']


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("is_active_version",)
