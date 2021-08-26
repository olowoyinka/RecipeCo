from datetime import datetime
from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import os
from django.core.paginator import Paginator
from django.db.models import Q

from chef_management_app.Form.recipeform import AddRecipeForm, EditRecipeForm
from chef_management_app.models import Appointment, ChefUser, Country, Recipe, RecipeImages, RecipeRating, RecipeCommentary, Payment


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


def GetRecipe(request):
    if request.method != "POST":
        chef = ChefUser.objects.get(admin = request.user.id)
        p = Paginator(Recipe.objects.filter(chefuser_id = chef).order_by('-id'), 6)
        page = request.GET.get('page')
        recipes = p.get_page(page)
        nums = "a" * recipes.paginator.num_pages

        recipes_ratings = []

        for recipe_obj in recipes:
            recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.id)
            total_rating = CalculateRating(recipe_rating_obj) + 1
            response = {
                "recipe" : recipe_obj,
                "rating" : total_rating,
            }
            recipes_ratings.append(response)
        return render(request, "recipe/get_recipe.html",  { "recipes" : recipes_ratings, 'nums' : nums })
    else:
        search = request.POST['search']

        if search:
            chef = ChefUser.objects.get(admin = request.user.id)
            p = Paginator(Recipe.objects.filter(Q(name__icontains = search) | Q(price__icontains = search)).order_by('-id'), 6)
            page = request.GET.get('page')
            recipes = p.get_page(page)
            nums = "a" * recipes.paginator.num_pages

            recipes_ratings = []

            for recipe_obj in recipes:
                recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.id)
                total_rating = CalculateRating(recipe_rating_obj) + 1
                response = {
                    "recipe" : recipe_obj,
                    "rating" : total_rating,
                }
                recipes_ratings.append(response)

            if recipes:
                return render(request, "recipe/get_recipe.html",  { "recipes" : recipes_ratings, 'nums' : nums })
            
            else:
                messages.error(request, "No result found")
                return render(request, "recipe/get_recipe.html") 
        else:
           return render(request, "recipe/get_recipe.html") 


def GetRecipeById(request, recipe_id):
    chef = ChefUser.objects.get(admin = request.user.id)
    recipe = Recipe.objects.get(chefuser_id = chef, id = recipe_id)

    recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe.id)

    total_rating = CalculateRating(recipe_rating_obj) + 1

    response = {
        "recipe" : recipe,
        "rating" : total_rating,
    }
        
    return render(request, "recipe/get_recipe_Id.html",  { "recipe" : response })


def CreateRecipe(request):
    if request.method!="POST":
        form = AddRecipeForm()
        return render(request, "recipe/create_recipe.html", { "form":form } )
    else:
        form = AddRecipeForm(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data["name"]
            description=form.cleaned_data["description"]
            method=form.cleaned_data["method"]
            ingredient=form.cleaned_data["ingredient"]
            price=form.cleaned_data["price"]
            period = form.cleaned_data["period"]
            address_name=form.cleaned_data["address_name"]
            country_id = form.cleaned_data["country"]

            if len(request.FILES) != 0:
                image_url = request.FILES['image_url']
            else:
                image_url =  None

            try:
                chef = ChefUser.objects.get(admin = request.user.id)
                country_obj = Country.objects.get(id=country_id)
                photo = Recipe.objects.create(
                    name=name,
                    decription=description,
                    method=method,
                    ingredient=ingredient,
                    price=price,
                    period = period,
                    address_name = address_name,
                    country_id = country_obj,
                    continent_id = country_obj.continent_id,
                    chefuser_id = chef,
                    image_url = image_url
                )
                messages.success(request,"Successfully Added New Recipe")
                return HttpResponseRedirect(reverse("get_recipe_Id", kwargs = { "recipe_id": photo.id }))
            except:
                messages.error(request,"Failed to Added New Recipe")
                return HttpResponseRedirect(reverse("create_recipe"))
        else:
            form = AddRecipeForm()(request.POST, request.FILES)
            return render(request, "recipe/create_recipe.html", {"form": form})



def EditRecipe(request, recipe_id):
    if request.method!="POST":
        chef = ChefUser.objects.get(admin = request.user.id)
        recipe = Recipe.objects.get(id = recipe_id , chefuser_id = chef)
        form = EditRecipeForm()
        form.fields['name'].initial = recipe.name
        form.fields['description'].initial = recipe.decription
        form.fields['method'].initial = recipe.method
        form.fields['ingredient'].initial = recipe.ingredient
        form.fields['price'].initial = recipe.price
        form.fields['period'].initial = recipe.period
        form.fields['address_name'].initial = recipe.name
        form.fields['country'].initial = recipe.country_id.id
        return render(request, "recipe/edit_recipe.html", { "form":form } )
    else:
        form = EditRecipeForm(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data["name"]
            description=form.cleaned_data["description"]
            method=form.cleaned_data["method"]
            ingredient=form.cleaned_data["ingredient"]
            price=form.cleaned_data["price"]
            period=form.cleaned_data["period"]
            address_name = form.cleaned_data["address_name"]
            country_id = form.cleaned_data["country"]
            

            try:
                chef = ChefUser.objects.get(admin = request.user.id)
                recipe = Recipe.objects.get(id = recipe_id , chefuser_id = chef)
                recipe.name = name
                recipe.decription = description
                recipe.method = method
                recipe.ingredient = ingredient
                recipe.price = price
                recipe.period = period

                recipe.address_name = address_name

                country_obj = Country.objects.get(id=country_id)
                recipe.country_id = country_obj
                recipe.continent_id = country_obj.continent_id

                if len(request.FILES) != 0:
                    os.remove(recipe.image_url.path)                
                    image_url = request.FILES['image_url']
                    recipe.image_url = image_url
                
                recipe.save()

                messages.success(request,"Successfully Edited Recipe")
                return HttpResponseRedirect(reverse("get_recipe_Id", kwargs = { "recipe_id":recipe_id }))
            except:
                messages.error(request,"Failed to Edit Recipe")
                return HttpResponseRedirect(reverse("edit_recipe", kwargs = { "recipe_id":recipe_id }))
        else:
            form = EditRecipeForm(request.POST,request.FILES)
            return render(request, "recipe/edit_recipe.html", {"form": form})


def DeleteRecipe(request, recipe_id):
    chef = ChefUser.objects.get(admin = request.user.id)
    recipe = Recipe.objects.get(id = recipe_id , chefuser_id = chef)
    if len(recipe.image_url) > 0:
        os.remove(recipe.image_url.path)
    recipe.delete()
    messages.success(request,"Delete Recipe")
    return HttpResponseRedirect(reverse("get_recipe"))


def FeatureRecipeImage(request, recipe_id):
    if request.method!="POST":
        chef = ChefUser.objects.get(admin = request.user.id)
        recipe = Recipe.objects.get(id = recipe_id , chefuser_id = chef)
        recipeImages = RecipeImages.objects.filter(recipe_id = recipe)
        return render(request,"recipe/feature_recipe_image.html", { "recipes": recipeImages })
    else:
        if request.user.id == None:
            return HttpResponseRedirect(reverse("home"))

        chef = ChefUser.objects.get(admin = request.user.id)
        recipe = Recipe.objects.get(id = recipe_id , chefuser_id = chef)

        images = request.FILES.getlist('images')

        for image in images:
            photo = RecipeImages.objects.create(
                url = image,
                recipe_id = recipe
            )

        try:
            messages.success(request,"Successfully Upload Multiple")
            return HttpResponseRedirect(reverse("feature_recipe_image", kwargs = { "recipe_id":recipe_id }))
        except:
            messages.error(request,"Failed to Upload Multiple")
            return HttpResponseRedirect(reverse("feature_recipe_image", kwargs = { "recipe_id":recipe_id }))


def DeleteFeatureRecipeImage(request, recipe_image_id):
    recipeImages = RecipeImages.objects.get(id = recipe_image_id)
    if len(recipeImages.url) > 0:
        os.remove(recipeImages.url.path)
    recipeImages.delete()
    messages.success(request,"Remove Image")
    return HttpResponseRedirect(reverse("feature_recipe_image", kwargs = { "recipe_id": recipeImages.recipe_id.id }))


def GetRecipeFeedBack(request, recipe_id):
    chef = ChefUser.objects.get(admin = request.user.id)
    recipe = Recipe.objects.get(chefuser_id = chef, id = recipe_id)

    recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe.id)

    p = Paginator(RecipeCommentary.objects.filter(recipe_id = recipe_id).order_by('-created_at'), 10)
    page = request.GET.get('page')
    recipeCommentary = p.get_page(page)
    nums = "a" * recipeCommentary.paginator.num_pages

    total_rating = CalculateRating(recipe_rating_obj) + 1

    response = {
        "recipe" : recipe.name,
        "rating" : range(total_rating),
        "ratingCount" : total_rating,
        "count" : recipe_rating_obj.count()
    }
        
    return render(request, "recipe/recipe_feedback.html",  { "recipe" : response, "commentary" : recipeCommentary, 'nums' : nums })





#Appointment
def GetBookingPending(request):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.filter(chefuser_id = chefuser, approved = False).order_by('-created_at')
    
    p = Paginator(appointment, 20)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    return render(request, "recipe/booking_pending.html", { "appointments" : appointments,  'nums' : nums })


def GetBookingResponse(request):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.filter(chefuser_id = chefuser, approved = True).order_by('-created_at')

    p = Paginator(appointment, 20)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    return render(request, "recipe/booking_approve.html", { "appointments" : appointments,  'nums' : nums })


def GetAllBookingPayment(request):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    payment = Payment.objects.filter(chefuser_id = chefuser, approved = True).order_by('-created_at')

    p = Paginator(payment, 20)
    page = request.GET.get('page')
    payments = p.get_page(page)
    nums = "a" * payments.paginator.num_pages

    return render(request, "recipe/get_all_booking_payment.html", { "payments" : payments,  'nums' : nums })


def GetBookingPayment(request,  payment_id):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    payment = Payment.objects.get(id = payment_id, chefuser_id = chefuser)

    return render(request, "recipe/get_booking_payment.html", { "payment" : payment })


def RecipeBookingConfirmation(request,  appointment_id):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.get(id = appointment_id, chefuser_id = chefuser)

    return render(request, "recipe/recipe_booking_confirmation.html", { "appointment" : appointment })


def BookingApproved(request, appointment_id):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.get(id = appointment_id, chefuser_id = chefuser)

    appointment.message = "Approved"
    appointment.created_at = datetime.now()
    appointment.approved = True

    appointment.save()
    messages.success(request,"Approved Appointment")
    return HttpResponseRedirect(reverse("chef_booking_confirmation", kwargs = { "appointment_id": appointment_id }))


def BookingDeclined(request, appointment_id):
    chefuser = ChefUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.get(id = appointment_id, chefuser_id = chefuser)

    appointment.message = "Declined"
    appointment.created_at = datetime.now()
    appointment.approved = True

    appointment.save()
    messages.error(request,"Declined Appointment")
    return HttpResponseRedirect(reverse("chef_booking_confirmation",  kwargs = { "appointment_id": appointment_id }))