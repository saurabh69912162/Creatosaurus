import unicodedata

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

# edit user
###############################################
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import *
from django import forms

User = get_user_model()



category_type= [
    ('Business', 'Business'),
    ('Creator', 'Creator'),
    ]




class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    first_name = forms.CharField(max_length=255, label='first_name')
    last_name = forms.CharField(max_length=255, label='last_name')
    category = forms.CharField(label='Category', widget=forms.Select(choices=category_type))
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name','category']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Username / Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does note exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("credentials are not correct")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("Password ::")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("<a href=\"{}\">Change Password</a>."),)

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class editpro(CustomUserChangeForm):

	class Meta:
		model = User
		fields = (
            'first_name',
            'last_name',
            'password'
        )




class busi_data(forms.ModelForm):

    class Meta:
        model = business_profile_data
        fields =(
            'company_category',
            'website',
            'number',
            'founded',
            'field_of_interest',
            'overview',
            'location',
            'address',
            'company_size',
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)



gender_type= [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ]



class creator_data(forms.ModelForm):
    gender = forms.CharField(label='Gender', widget=forms.Select(choices=gender_type))
    class Meta:
        model = creator_profile_data
        fields =(
            'artist_category',
            'skills',
            'description',
            'gender',
            'website',
            'number',
            'address',
            'location',

        )
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)




class temp_data_form(forms.ModelForm):
    img = forms.ImageField(required=False)
    class Meta:
        model = temp_data
        fields = {'img',}


class reschedluer(forms.ModelForm):
    class Meta:
        model = scheduler_model
        fields = {'image',}


