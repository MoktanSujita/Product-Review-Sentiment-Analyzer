from django import forms

class ReviewForm(forms.Form):
    url = forms.URLField(label='Product URL', max_length=200, required=True)
    review_text = forms.CharField(label='Review Text', widget=forms.Textarea, required=True)