from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os


from chef_management_app.Form.chefform import EditChefForm
from chef_management_app.models import CustomUser, ChefUser, ChefImages, Country


def HomePage(request):
    return render(request, "Chef/home.html")


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
        return render(request,"chef/edit_chef.html", {"form":form, "username":chefuser.admin.username, "email":chefuser.admin.email })
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

                messages.success(request,"Successfully Edited Chef")
                return HttpResponseRedirect(reverse("edit_chef"))
            except:
                messages.error(request,"Failed to Edit Chef")
                return HttpResponseRedirect(reverse("edit_chef"))
        else:
            form = EditChefForm(request.POST)
            chefuser = ChefUser.objects.get(admin = request.user.id)
            return render(request,"chef/edit_chef.html", {"form":form, "username":chefuser.admin.username, "email":chefuser.admin.email})


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
            messages.success(request,"Successfully Edited User")
            return HttpResponseRedirect(reverse("chef_image"))
        except:
            messages.error(request,"Failed to Edit User")
            return HttpResponseRedirect(reverse("chef_image"))
 

def RemoveImageChef(request):
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))            

        try:
            chef = ChefUser.objects.get(admin = request.user.id)
            if chef.image_url != "chef/login-img.png":
                os.remove(chef.image_url.path)
            chef.image_url = "chef/login-img.png"
            chef.save()

            messages.success(request,"Successfully Remove User Image")
            return HttpResponseRedirect(reverse("chef_image"))
        except:
            messages.error(request,"Failed to Remove User Image")
            return HttpResponseRedirect(reverse("chef_image"))


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