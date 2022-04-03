import django.forms as forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email_is_not_taken(value):
    if User.objects.filter(email=value):
        raise ValidationError("Istnieje już konto o podanym emailu")


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}), validators=[validate_email_is_not_taken])
    pass1 = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    pass2 = forms.CharField(label='', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-group'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['pass1'] != cleaned_data['pass2']:
            raise ValidationError('Hasła muszą być takie same')
        return cleaned_data
