# Create your views here.
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin, ProcessFormView

from forms.forms import ContactForm


class ContactFormView(FormMixin, ProcessFormView):
    http_method_names = ['options', 'post']
    form_class = ContactForm

    def form_valid(self, form):
        data = form.clean()
        topic = data['topic']
        subject = "[SFI.PL] " + topic
        content = data['message']
        sender_name = data['name']
        sender_email = data['email']

        message = f'Message from {sender_name} ({sender_email}) submitted via sfi.pl.\n' \
                  f'Subject: {topic}\n==========\n{content}'
        send_mail(subject=subject, message=message, recipient_list=[settings.CONTACT_EMAIL],
                  from_email=settings.SERVER_EMAIL)
        return HttpResponse()

    def form_invalid(self, form):
        return HttpResponse(form.errors.as_json(), status=400)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
