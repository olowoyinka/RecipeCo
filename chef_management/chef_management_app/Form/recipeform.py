from django import forms
from chef_management_app.models import Country
from ckeditor.widgets import CKEditorWidget


class AddRecipeForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    description=forms.CharField(label="Description",widget=CKEditorWidget(attrs={"class":"form-control"}))
    method=forms.CharField(label="Method",widget=CKEditorWidget(attrs={"class":"form-control"}))
    ingredient=forms.CharField(label="Ingredient",widget=CKEditorWidget(attrs={"class":"form-control"}))
    price=forms.IntegerField(label="Price",widget=forms.NumberInput(attrs={"class":"form-control"}))

    image_url=forms.FileField(label="Main Image",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
    address_name = forms.CharField(label="Address Location",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.id, country.name)
        country_list.append(small_couuntry)
    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control"}))


class EditRecipeForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    description=forms.CharField(label="Description",widget=CKEditorWidget(attrs={"class":"form-control"}))
    method=forms.CharField(label="Method",widget=CKEditorWidget(attrs={"class":"form-control"}))
    ingredient=forms.CharField(label="Ingredient",widget=CKEditorWidget(attrs={"class":"form-control"}))
    price=forms.IntegerField(label="Price",widget=forms.NumberInput(attrs={"class":"form-control"}))

    image_url=forms.FileField(label="Main Image",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}), required=False)
    address_name = forms.CharField(label="Address Location",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.id, country.name)
        country_list.append(small_couuntry)
    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control"}))
