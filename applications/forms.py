from django import forms
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import requests
import hashlib

from .models import Application, Answer, Question, Score, Email
from .utils import generate_form_from_questions
from core.forms import BetterReCaptchaField


class ApplicationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        """
        The form here is programatically generated out of Question objects
        """
        self.form = kwargs.pop('form')
        self.base_fields = generate_form_from_questions(
            self.form.question_set.all())
        self.base_fields.update({
            'captcha': BetterReCaptchaField()
        })
        super(ApplicationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = None
        field_name = None

        for name in self.cleaned_data:
            question = None
            pk = name.replace('question_', '')
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=self.form)
            except (Question.DoesNotExist, ValueError):
                continue

            if question and question.question_type == 'email':
                email = value
                field_name = name
                break

        if email is not None:
            if (Application.objects
                    .filter(form=self.form, email=email)
                    .exists()):
                self.add_error(field_name,
                               'Application for this e-mail already exists.')

        # Always return cleaned_data
        return cleaned_data

    def save(self, *args, **kwargs):
        application = Application.objects.create(form=self.form)

        for name in self.cleaned_data:
            question = None
            pk = name.replace('question_', '')
            value = self.cleaned_data[name]
            try:
                question = Question.objects.get(pk=pk, form=self.form)
            except (Question.DoesNotExist, ValueError):
                if name == 'newsletter_optin':
                    if value == 'yes':
                        application.newsletter_optin = True
                    else:
                        application.newsletter_optin = False
                    application.save()

            value = ', '.join(value) if type(value) == list else value

            if question:
                Answer.objects.create(
                    application=application,
                    question=question,
                    answer=value
                )

                if question.question_type == 'email':
                    application.email = value
                    application.save()

        if not self.form.page.event.email:
            # If event doesn't have an email (legacy events), create
            # it just by taking the url. In 99% cases, it is correct.
            self.form.page.event.email = "{}@djangogirls.org".format(
                self.form.page.url)
            self.form.page.event.save()

        if application.email:
            # Send confirmation email
            subject = "Confirmation of your application for {}".format(
                self.form.page.title)
            body = render_to_string(
                'emails/application_confirmation.html',
                {
                    'application': application,
                    'intro': self.form.confirmation_mail,
                }
            )
            msg = EmailMessage(subject, body, self.form.page.event.email, [
                               application.email, ])
            msg.content_subtype = "html"
            try:
                msg.send()
            except:
                # TODO: what should we do when sending fails?
                pass

        # Adding applicant email to Django Girls Dispatch
        if application.newsletter_optin and application.email:
            emailb = application.email.encode()
            emailhash = hashlib.md5(emailb).hexdigest()
            r = requests.get("https://us8.api.mailchimp.com/3.0/lists/d278270e6f/members/%s" %
                             emailhash, auth=('user', settings.MAILCHIMP_API_KEY))
            # Mailchimp will return a 404 if the email we want to add is not on
            # the Dispatch subscriber list
            if r.status_code == 404:
                url = "https://us8.api.mailchimp.com/3.0/lists/d278270e6f/members/"
                payload = {"email_address": application.email,
                           "status": "pending"}
                requests.post(url, auth=(
                    'user', settings.MAILCHIMP_API_KEY), json=payload)


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['score', 'comment']


class EmailForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        When email is already sent, the form should be disabled
        """
        super(EmailForm, self).__init__(*args, **kwargs)
        if self.instance.sent:
            # email was sent, let's disable all fields:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = True

    class Meta:
        model = Email
        fields = ['recipients_group', 'subject', 'text']
