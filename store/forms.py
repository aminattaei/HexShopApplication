from django import forms
from .models import Contact, Comment, ShippingAddress



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ("fullname", "email", "message")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ("country", "city", "address", "zipcode")
