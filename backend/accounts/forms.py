from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import RegularAccount


class RegularAccountCreationForm(UserCreationForm):

    class Meta:
        model = RegularAccount
        fields = ('username',)


class RegularAccountChangeForm(UserChangeForm):

    class Meta:
        model = RegularAccount
        fields = ('username',)
