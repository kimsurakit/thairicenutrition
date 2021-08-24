from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _

class CoreSignupForm(SignupForm):
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": _("First Name"), "autocomplete": "first_name"}
        ),
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": _("Last Name"), "autocomplete": "last_name"}
        ),
    )
    institute = forms.CharField(
        label=_("Institute"),
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": _("Institute"), "autocomplete": "institute"}
        ),
    )
    def custom_signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.institute = self.cleaned_data['institute']
        user.save()
