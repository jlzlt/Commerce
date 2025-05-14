import requests
from django import forms
from django.core.exceptions import ValidationError

from .models import Comments


def validate_image_url(url):
    try:
        response = requests.head(url, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            raise ValidationError("URL does not point to a valid image.")
    except requests.RequestException:
        raise ValidationError("Could not reach the image URL.")


class CreateListingForm(forms.Form):
    title = forms.CharField(
        label="Title", 
        required=True, 
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control create_fields'})
    )
    start_bid = forms.DecimalField(
        label="Starting Bid ($)", 
        required=True,
        min_value=0, 
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'form-control create_fields'})
    )
    pic_url = forms.URLField(
        label="Picture URL (optional)", 
        required=False, 
        max_length=255,
        validators=[validate_image_url],
        widget=forms.TextInput(attrs={'class': 'form-control create_fields'})
    )
    category = forms.CharField(
        label="Category (optional)", 
        required=False, 
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control create_fields'})
    )
    description = forms.CharField(
        label="Description", 
        widget=forms.Textarea(attrs={'id': 'create_desc', 'class': 'form-control'}), 
        required=True, 
        max_length=1000
    )


class PlaceBidForm(forms.Form):
    bid = forms.DecimalField(
        label='Place a bid',
        max_digits=8,
        decimal_places=2,
        min_value=0.01,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bid',
        })
    )

    def __init__(self, *args, current_bid=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_bid = current_bid

    def clean_bid(self):
        bid = self.cleaned_data.get('bid')
        if self.current_bid is not None and bid <= self.current_bid:
            raise ValidationError(f'Your bid must be higher than the current price (${self.current_bid:.2f}).')
        return bid
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
            })
        }
        labels = {
            'comment': ''
        }