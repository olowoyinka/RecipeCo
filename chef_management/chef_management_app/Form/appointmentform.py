import datetime
from django import forms
from django.core import validators
from django.core.validators import MinValueValidator


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class CreateAppointmentForm(forms.Form):
    booking_time = forms.TimeField(label="Select a time", widget=TimeInput(attrs={"class":"form-control", "placeholder": "Select a time"}))
    booking_date = forms.DateField(label="Select a date", validators = [MinValueValidator(datetime.date.today)], widget=DateInput(attrs={"class":"form-control", "placeholder": "Select a date"}))
    quantity = forms.IntegerField(label="Quantity needed", widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "Quantity needed"}))
    address = forms.CharField(label="Address", max_length = 255, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Address"}))



class EditAppointmentForm(forms.Form):
    booking_time = forms.TimeField(label="Select a time", widget=forms.TimeInput(attrs={"class":"form-control", "placeholder": "Select a time"}))
    booking_date = forms.DateField(label="Select a date", validators = [MinValueValidator(datetime.date.today)], widget=forms.DateInput(attrs={"class":"form-control", "placeholder": "Select a date"}))
    quantity = forms.IntegerField(label="Quantity needed", widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "Quantity needed"}))
    address = forms.CharField(label="Address", max_length = 255, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Address"}))



class CreatePaymentForm(forms.Form):
    card_number = forms.IntegerField(label="Card number", widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "Card number"}))
    month = forms.CharField(label="Select a month", widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "valid month"}) , required = False)
    cvv = forms.IntegerField(label="CVV", widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "CVV"}))
    pin = forms.CharField(label="PIN",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "PIN"}))