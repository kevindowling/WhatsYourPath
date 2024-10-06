from django import forms

class PromptForm(forms.Form):
    prompt = forms.CharField(
        label='Enter your prompt',
        widget=forms.Textarea(attrs={'rows': 6, 'cols': 80})
    )
