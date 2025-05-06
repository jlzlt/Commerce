import requests
from django import forms
from django.core.exceptions import ValidationError


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
        widget=forms.TextInput(attrs={'class': 'create_fields'})
    )
    start_bid = forms.DecimalField(
        label="Starting Bid", 
        required=True,
        min_value=0, 
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'create_fields'})
    )
    pic_url = forms.URLField(
        label="Picture URL", 
        required=False, 
        max_length=255,
        validators=[validate_image_url],
        widget=forms.TextInput(attrs={'class': 'create_fields'})
    )
    category = forms.CharField(
        label="Category", 
        required=False, 
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'create_fields'})
    )
    description = forms.CharField(
        label="Description", 
        widget=forms.Textarea(attrs={'id': 'create_desc'}), 
        required=True, 
        max_length=1000
    )