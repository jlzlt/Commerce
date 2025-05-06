from django import forms


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