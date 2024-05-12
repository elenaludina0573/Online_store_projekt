from django.contrib.auth.forms import UserCreationForm
from django.forms import BooleanField

from catalog.forms import StyleFormMixin
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterFrom(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


