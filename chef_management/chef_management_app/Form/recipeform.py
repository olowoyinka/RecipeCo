from django import forms
from chef_management_app.models import Country
from ckeditor.widgets import CKEditorWidget


class AddRecipeForm(forms.Form):
    image_url=forms.FileField(label="Select meal photo",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
    name=forms.CharField(label="Recipe name",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    price=forms.IntegerField(label="Recipe Price",widget=forms.NumberInput(attrs={"class":"form-control"}))
    period=forms.IntegerField(label="Recipe Duration In Minutes",widget=forms.NumberInput(attrs={"class":"form-control"}))
    description=forms.CharField(label="Description",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)
    address_name = forms.CharField(label="Address Location (Optional)",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.id, country.name)
        country_list.append(small_couuntry)
    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control"}))
    
    ingredient=forms.CharField(label="Ingredients",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)
    method=forms.CharField(label="Method",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)


class EditRecipeForm(forms.Form):
    name=forms.CharField(label="Name",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}))
    description=forms.CharField(label="Description",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)
    method=forms.CharField(label="Method",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)
    ingredient=forms.CharField(label="Ingredient",widget=CKEditorWidget(attrs={"class":"form-control"}), required=True)
    price=forms.IntegerField(label="Price",widget=forms.NumberInput(attrs={"class":"form-control"}))
    period=forms.IntegerField(label="Recipe Duration In Minutes",widget=forms.NumberInput(attrs={"class":"form-control"}))

    image_url=forms.FileField(label="Main Image",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}), required=False)
    address_name = forms.CharField(label="Address Location",max_length=100,widget=forms.TextInput(attrs={"class":"form-control"}), required=False)

    countries = Country.objects.all().order_by('name')
    country_list = []
    for country in countries:
        small_couuntry = (country.id, country.name)
        country_list.append(small_couuntry)
    country = forms.ChoiceField(label="Country",choices=country_list,widget=forms.Select(attrs={"class":"form-control"}))
