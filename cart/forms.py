# Add this to your forms.py file (or create one if it doesn't exist)

from django import forms
from .models import CheckoutFeedback

class CheckoutFeedbackForm(forms.ModelForm):
    class Meta:
        model = CheckoutFeedback
        fields = ['name', 'feedback_text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional - leave blank to remain anonymous)',
                'maxlength': '100'
            }),
            'feedback_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts about the checkout process...',
                'rows': 4,
                'maxlength': '500',
                'required': True
            })
        }
        labels = {
            'name': 'Name (Optional)',
            'feedback_text': 'How was your checkout experience?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['feedback_text'].required = True