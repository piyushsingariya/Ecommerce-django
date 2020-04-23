from django import forms

PAYMENT_OPT = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'B64 KK Colony',
        'class': 'form-control'
    }))
    address2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    district = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_Options = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPT)
