from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

import os


from chef_management_app.Form.regularuserform import EditRegularUserForm, EditRegularUserImageForm
from chef_management_app.models import CustomUser, RegularUser



def HomePage(request):
    return render(request, "RegularUser/home.html")


def EditRegularUser(request):
    if request.method!="POST":
        regularuser = RegularUser.objects.get(admin = request.user.id)
        form = EditRegularUserForm()
        form.fields['first_name'].initial = regularuser.admin.first_name
        form.fields['last_name'].initial = regularuser.admin.last_name
        form.fields['phone_number'].initial = regularuser.phone_number
        return render(request,"regularuser/edit_user.html", {"form":form, "username":regularuser.admin.username, "email":regularuser.admin.email })

    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        form = EditRegularUserForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]

            try:
                user = CustomUser.objects.get(id = request.user.id)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                regularuser = RegularUser.objects.get(admin = request.user.id)
                regularuser.phone_number = phone_number
                regularuser.save()

                messages.success(request,"Successfully Edited User")
                return HttpResponseRedirect(reverse("edit_user"))
            except:
                messages.error(request,"Failed to Edit User")
                return HttpResponseRedirect(reverse("edit_user"))
        else:
            form = EditRegularUserForm(request.POST)
            regularuser = RegularUser.objects.get(admin = request.user.id)
            return render(request,"regularuser/edit_user.html", {"form":form, "username":regularuser.admin.username, "email":regularuser.admin.email})


def ImageRegularUser(request):
    if request.method!="POST":
        regularuser = RegularUser.objects.get(admin = request.user.id)
        return render(request,"regularuser/user_image.html", { "email":regularuser.admin.email, "image_url":regularuser.image_url })
    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        regularuser = RegularUser.objects.get(admin = request.user.id)

        if len(request.FILES) != 0:
            if len(regularuser.image_url) > 0:
                if regularuser.image_url != "user/login-img.png":
                    os.remove(regularuser.image_url.path)
                    regularuser.image_url = request.FILES['image_url']
                else:
                    regularuser.image_url = request.FILES['image_url']
        else:
            regularuser.image_url =  None

        try:
            regularuser.save()
            messages.success(request,"Successfully Edited User")
            return HttpResponseRedirect(reverse("user_image"))
        except:
            messages.error(request,"Failed to Edit User")
            return HttpResponseRedirect(reverse("user_image"))
 


def RemoveImageRegularUser(request):
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))            

        try:
            regularuser = RegularUser.objects.get(admin = request.user.id)
            if regularuser.image_url != "user/login-img.png":
                os.remove(regularuser.image_url.path)
            regularuser.image_url = "user/login-img.png"
            regularuser.save()

            messages.success(request,"Successfully Remove User Image")
            return HttpResponseRedirect(reverse("user_image"))
        except:
            messages.error(request,"Failed to Remove User Image")
            return HttpResponseRedirect(reverse("user_image"))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email = email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)