from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os


from chef_management_app.Form.chefform import EditChefForm
from chef_management_app.models import CustomUser, ChefUser, ChefImages, Country, Appointment, Recipe, RecipeRating, Payment



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



def HomePages(request):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    count_appointment = Appointment.objects.filter(chefuser_id = chefuser).count()
    appointment = Appointment.objects.filter(chefuser_id = chefuser, message = "Pending").order_by("-created_at")
    recent_appointment = appointment[:6]
    payment_appointment = Payment.objects.filter(chefuser_id = chefuser, message = "Payment Successful").count()
    recipes = Recipe.objects.filter(chefuser_id = chefuser).order_by('-created_at')[:3]
    total_appointment = count_appointment + payment_appointment
    recipes_ratings = []
    for recipe_obj in recipes:
        recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.id)
        total_rating = CalculateRating(recipe_rating_obj) + 1
        response = {
            "recipe" : recipe_obj,
            "rating" : total_rating,
        }
        recipes_ratings.append(response)
    return render(request, "Chef/home.html", { "count_appointment" : total_appointment,  "pending_appointment" : count_appointment, "payment_appointment" : payment_appointment, "recipes" : recipes_ratings, "recent_appointment" : recent_appointment })



def EditChef(request):
    if request.method!="POST":
        chefuser = ChefUser.objects.get(admin = request.user.id)
        form = EditChefForm()
        form.fields['first_name'].initial = chefuser.admin.first_name
        form.fields['last_name'].initial = chefuser.admin.last_name
        form.fields['chef_name'].initial = chefuser.chef_name
        form.fields['phone_number'].initial = chefuser.phone_number
        form.fields['address_name'].initial = chefuser.address_name
        form.fields['country'].initial = chefuser.country_id.id
        return render(request,"chef/edit_chef.html", {"form":form, "username":chefuser.admin.username, "email":chefuser.admin.email, "image_url":chefuser.image_url })
    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        form = EditChefForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            chef_name = form.cleaned_data["chef_name"]

            phone_number = form.cleaned_data["phone_number"]
            address_name = form.cleaned_data["address_name"]
            country_id = form.cleaned_data["country"]

            try:
                user = CustomUser.objects.get(id = request.user.id)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                chefuser = ChefUser.objects.get(admin = request.user.id)
                chefuser.chef_name = chef_name
                chefuser.phone_number = phone_number
                chefuser.address_name = address_name

                country_obj = Country.objects.get(id=country_id)
                chefuser.country_id = country_obj
                chefuser.continent_id = country_obj.continent_id

                chefuser.save()

                messages.success(request,"Successfully Update Profile")
                return HttpResponseRedirect(reverse("edit_chef"))
            except:
                messages.error(request,"Failed to Update Profile")
                return HttpResponseRedirect(reverse("edit_chef"))
        else:
            form = EditChefForm(request.POST)
            chefuser = ChefUser.objects.get(admin = request.user.id)
            return render(request,"chef/edit_chef.html", {"form":form, "username":chefuser.admin.username, "email":chefuser.admin.email, "image_url":chefuser.image_url})



def ImageChef(request):
    if request.method!="POST":
        chef = ChefUser.objects.get(admin = request.user.id)
        return render(request,"chef/chef_image.html", { "email":chef.admin.email, "image_url":chef.image_url })
    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        chef = ChefUser.objects.get(admin = request.user.id)

        if len(request.FILES) != 0:
            if len(chef.image_url) > 0:
                if chef.image_url != "chef/login-img.png":
                    os.remove(chef.image_url.path)
                    chef.image_url = request.FILES['image_url']
                else:
                    chef.image_url = request.FILES['image_url']
        else:
            chef.image_url =  None

        try:
            chef.save()
            messages.success(request,"Successfully Upload Image")
            return HttpResponseRedirect(reverse("edit_chef"))
        except:
            messages.error(request,"Failed to Upload Image")
            return HttpResponseRedirect(reverse("edit_chef"))
 

def RemoveImageChef(request):
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))            

        try:
            chef = ChefUser.objects.get(admin = request.user.id)
            if chef.image_url != "chef/login-img.png":
                os.remove(chef.image_url.path)
            chef.image_url = "chef/login-img.png"
            chef.save()

            messages.success(request,"Successfully Remove Profile")
            return HttpResponseRedirect(reverse("edit_chef"))
        except:
            messages.error(request,"Failed to Remove Profile")
            return HttpResponseRedirect(reverse("edit_chef"))


def FeatureImageChef(request):
    if request.method!="POST":
        chef = ChefUser.objects.get(admin = request.user.id)
        chefimage = ChefImages.objects.filter(chefuser_id = chef)
        return render(request,"chef/feature_chef_image.html", { "chefs": chefimage })
    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        chef = ChefUser.objects.get(admin = request.user.id)

        images = request.FILES.getlist('images')

        for image in images:
            photo = ChefImages.objects.create(
                url = image,
                chefuser_id = chef
            )

        try:
            messages.success(request,"Successfully Upload Multiple")
            return HttpResponseRedirect(reverse("feature_chef_image"))
        except:
            messages.error(request,"Failed to Upload Multiple")
            return HttpResponseRedirect(reverse("feature_chef_image"))


def RemoveFeatureImageChef(request, chef_image_id):
    chef = ChefUser.objects.get(admin = request.user.id)
    chefimage = ChefImages.objects.get(id = chef_image_id, chefuser_id = chef)
    if len(chefimage.url) > 0:
        os.remove(chefimage.url.path)
    chefimage.delete()
    messages.success(request,"Remove Image")
    return HttpResponseRedirect(reverse("feature_chef_image"))