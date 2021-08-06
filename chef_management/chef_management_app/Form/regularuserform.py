from django import forms



class UserLoginForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "email", "autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "password"}))


class AddRegularUserForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "email", "autocomplete":"off"}))
    confirm_email=forms.EmailField(label="Retype Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "retypeemail", "autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "password"}))
    confirm_password=forms.CharField(label="Confirm Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder": "confirmpassword"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "firstname"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "lastname"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "username"}))
    confirm_username=forms.CharField(label="Retype Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder": "retypeusername"}))
    phone_number=forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control", "placeholder": "phonenumber"}))

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


class EditRegularUserForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    phone_number=forms.IntegerField(label="Phone Number",widget=forms.NumberInput(attrs={"class":"form-control"}))


class EditRegularUserImageForm(forms.Form):
    image_url=forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))