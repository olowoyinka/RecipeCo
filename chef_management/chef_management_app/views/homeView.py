from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core import exceptions
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings


from chef_management_app.EmailBackEnd import EmailBackEnd
from chef_management_app.Form.chefform import AddChefForm
from chef_management_app.Form.regularuserform import AddRegularUserForm, UserLoginForm
from chef_management_app.models import CustomUser, Country , Recipe, RecipeRating, ChefUser
from chef_management_app.utils import generate_token


def CalculateRating(ratings):
    rating_initial = 0
    sum_divid = 1
    for rating in ratings:
        if rating.rating == 5:
            rating_initial = (5 * 5) + rating_initial
            sum_divid = sum_divid + 5
        elif rating.rating == 4:
            rating_initial = (4 * 4) + rating_initial
            sum_divid = sum_divid + 4
        elif rating.rating == 3:
            rating_initial = (3 * 3) + rating_initial
            sum_divid = sum_divid + 3
        elif rating.rating == 2:
            rating_initial = (2 * 2) + rating_initial
            sum_divid = sum_divid + 2
        elif rating.rating == 1:
            rating_initial = (1 * 1) + rating_initial
            sum_divid = sum_divid + 1
        else:
            rating_initial = (0 * 0) + rating_initial
            sum_divid = sum_divid + 0
    total_num = (rating_initial) / (sum_divid)
    return int(total_num)

def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your chef management'
    email_body = render_to_string('home/activate.html', {
        'user' : user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject = email_subject,
        body = email_body,
        from_email = settings.EMAIL_FROM_USER,
        to = [user.email]
    )

    email.send()

# Create your views here.
def HomePage(request):
    recipes = Recipe.objects.all().order_by('?')[:4]
    chefusers = ChefUser.objects.all().order_by('?')[:4]
    countries = Country.objects.all().order_by('?')[:3]
    recipes_ratings = []
    for recipe_obj in recipes:
        recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.id)
        total_rating = CalculateRating(recipe_rating_obj) + 1
        response = {
            "recipe" : recipe_obj,
            "rating" : total_rating,
        }
        recipes_ratings.append(response)
    return render(request, "Home/welcome.html",  { "recipes" : recipes_ratings, "countries" : countries, "chefusers" : chefusers })
 

def Login(request):
    if request.method!="POST":
        form = UserLoginForm()
        return render(request, "Home/login.html", { "form":form })
    else:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user = EmailBackEnd.authenticate(request, username=email, password=password)
            
            if user != None:
                login(request,user)
                if not user.is_active:
                    messages.error(request,"Email is not verified, check your email")
                    return HttpResponseRedirect(reverse("login"))
                if user.user_type == "1":
                    return HttpResponseRedirect(reverse('admin_home'))
                elif user.user_type == "2":
                    return HttpResponseRedirect(reverse("chef_home"))
                else:
                    return HttpResponseRedirect(reverse("user_home"))
            else:
                messages.error(request,"Invalid Login Details")
                return HttpResponseRedirect(reverse("login"))
        else:
            form = UserLoginForm(request.POST)
            return render(request, "Home/login.html", { "form":form })
 

def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))



def ChefRegister(request):
    if request.method!="POST":
        form = AddChefForm()
        return render(request, "chef/register.html", { "form":form } )
    else:
        form = AddChefForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            chef_name=form.cleaned_data["chef_name"]
            phone_number=form.cleaned_data["phone_number"]
            address_name=form.cleaned_data["address_name"]
            country_id = form.cleaned_data["country"]

            try:          
                user_email_exist = CustomUser.objects.filter(email = email).exists()
                if user_email_exist:
                    messages.error(request,"Email Address already exist")
                    return HttpResponseRedirect(reverse("chef_register"))

                user_username_exist = CustomUser.objects.filter(username = username).exists()
                if user_username_exist:
                    messages.error(request,"Username already exist")
                    return HttpResponseRedirect(reverse("chef_register"))

                user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                country_obj = Country.objects.get(id=country_id)
                user.chefuser.chef_name = chef_name
                user.chefuser.phone_number = phone_number
                user.chefuser.address_name = address_name
                user.chefuser.country_id = country_obj
                user.chefuser.continent_id = country_obj.continent_id
                user.chefuser.image_url = "chef/login-img.png"
                user.is_active = True
                user.save()

                #send_action_email(user, request)

                messages.success(request,"Check Your Email to verified account")
                return HttpResponseRedirect(reverse("login"))
            except:
                messages.error(request,"Failed to Register New User")
                return HttpResponseRedirect(reverse("user_register"))
          
        else:
            form = AddChefForm(request.POST)
            return render(request, "chef/register.html", {"form": form})


def RegularUserRegister(request):
    if request.method!="POST":
        form = AddRegularUserForm()
        return render(request, "regularuser/register.html", { "form":form } )
    else:
        form = AddRegularUserForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            phone_number=form.cleaned_data["phone_number"]
            country_id = form.cleaned_data["country"]

            try:
                user_email_exist = CustomUser.objects.filter(email = email).exists()
                if user_email_exist:
                    messages.error(request,"Email Address already exist")
                    return HttpResponseRedirect(reverse("user_register"))
                
                user_username_exist = CustomUser.objects.filter(username = username).exists()
                if user_username_exist:
                    messages.error(request,"Username already exist")
                    return HttpResponseRedirect(reverse("user_register"))

                country_obj = Country.objects.get(id=country_id)
                user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.regularuser.phone_number = phone_number
                user.regularuser.country_id = country_obj
                user.regularuser.continent_id = country_obj.continent_id
                user.regularuser.image_url = "user/login-img.png"
                user.is_active = True
                user.save()
                
                #send_action_email(user, request)

                messages.success(request,"Check Your Email to verified account")
                return HttpResponseRedirect(reverse("login"))
            except:
                messages.error(request,"Failed to Register New User")
                return HttpResponseRedirect(reverse("user_register"))
        else:
            form = AddRegularUserForm(request.POST)
            return render(request, "regularuser/register.html", {"form": form})


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = CustomUser.objects.get(pk = uid)
    
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Email verified, you can now login")
        return HttpResponseRedirect(reverse("login"))
    
    return render(request , 'home/activate_failed.html', {"user": user})


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email = email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username = username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)