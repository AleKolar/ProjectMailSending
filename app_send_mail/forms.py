from django import forms

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=200, label='Subject')
    body = forms.CharField(widget=forms.Textarea, label='Body (HTML)')