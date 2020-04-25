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
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPT)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria - label': 'Recipient\'s username',
        'aria - describedby': 'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'placeholder': 'Please specify the reason here!'
    }))
    email = forms.EmailField()