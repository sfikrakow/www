from captcha.fields import ReCaptchaField
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    topic = forms.CharField(max_length=200)
    message = forms.CharField(max_length=1000)
# captcha = ReCaptchaField(required=False)  # TODO: switch to true
