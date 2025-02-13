from django import forms

from app_send_mail.models import Subscriber


class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=200, label='Subject')
    body = forms.CharField(widget=forms.Textarea, label='Body (HTML)')

class SubscriberRegistrationForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Subscriber
        fields = ['email', 'first_name', 'last_name', 'birthday']

    def save(self, commit=True):
        subscriber = super(SubscriberRegistrationForm, self).save(commit=False)
        if commit:
            subscriber.save()
        return subscriber