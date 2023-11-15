from django import forms
from django.forms import ModelForm, widgets
from myapp.models import Order


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
