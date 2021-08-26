from django import forms
from chef_management_app.models import Country



class SearchCountryForm(forms.Form):
    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.name, country.name)
        country_list.append(small_couuntry)
        
    country = forms.ChoiceField(label = "Country", choices = country_list, widget = forms.Select(attrs={"class":"form-control"}))

    searches = forms.CharField(label = "Search", max_length = 100, widget = forms.TextInput(attrs={"class":"form-control"}), required = False)