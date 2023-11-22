from django import forms
from django.forms import ModelForm, widgets
from myapp.models import Order
from django.contrib.auth.forms import AuthenticationForm



class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]

    interested = forms.TypedChoiceField(
        label='Are you interested?',
        choices=INTEREST_CHOICES,
        widget=forms.RadioSelect,
        coerce=int,
    )

    levels = forms.IntegerField(
        label='How many levels are you interested in?',
        initial=1,
        min_value=1,
        max_value=3,
    )

    comments = forms.CharField(
        label='Additional Comments',
        widget=forms.Textarea,
        required=False,
    )


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']

        widgets = {
            'student': forms.RadioSelect,
            'order_date': forms.SelectDateWidget,
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = None  # No model is associated with this form
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Password"}
        )
