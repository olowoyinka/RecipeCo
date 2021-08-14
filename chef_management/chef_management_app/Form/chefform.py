from django import forms
from chef_management_app.models import Country



class AddChefForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "email", "autocomplete":"off"}))
    confirm_email=forms.EmailField(label="Retype Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "retypeemail", "autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "password"}))
    confirm_password=forms.CharField(label="Retype Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "confirmpassword"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "firstname"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "lastname"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "username"}))
    confirm_username=forms.CharField(label="Retype Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "retypeusername"}))
    chef_name=forms.CharField(label="Chef Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "chefname"}))
    phone_number=forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "phonenumber"}))
    address_name = forms.CharField(label="Address Location",max_length=100,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "addressname"}))

    countries = Country.objects.all().order_by('name')
    country_list = [('','')]
    for country in countries:
        small_couuntry = (country.id, country.name) 
        country_list.append(small_couuntry)

    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control", "placeholder": "country"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        username = cleaned_data.get('username')
        confirm_username = cleaned_data.get('confirm_username')
        
        if email != confirm_email:
            raise forms.ValidationError('Email do not match')
        
        if password != confirm_password:
            raise forms.ValidationError('Password do not match')
        
        if username != confirm_username:
            raise forms.ValidationError('Username do not match')


class EditChefForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    chef_name=forms.CharField(label="Chef Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control"}))
    address_name = forms.CharField(label="Address Location",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))

    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.id, country.name)
        country_list.append(small_couuntry)
        
    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control"}))