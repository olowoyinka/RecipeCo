from datetime import datetime
from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

from chef_management_app.models import ChefUser, Continent, RecipeCommentary, Recipe, RecipeImages, RegularUser, RecipeRating, Country, RecipeFavorite, RegularUserFavorite, Appointment, Payment
from chef_management_app.Form.appointmentform import CreateAppointmentForm, EditAppointmentForm, CreatePaymentForm



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



def HomePage(request):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    recipes = Recipe.objects.filter(continent_id = regularuser.continent_id).order_by('?')[:8]
    chefs = ChefUser.objects.filter(continent_id = regularuser.continent_id).order_by('?')[:8]
    continent = Continent.objects.all().order_by('name')
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
    return render(request, "userrecipe/home.html",  { "recipes" : recipes_ratings, "countries" : countries, "continent" : continent, "chefs" : chefs })



def RecipeResult(request, search):
    if request.method != "POST":
        continent = Continent.objects.get(name = search)
        p = Paginator(Recipe.objects.filter(continent_id = continent).order_by('?'), 20)
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
        return render(request, "userrecipe/recipe_result.html",  { "recipes" : recipes_ratings, "message" : search, 'nums' : nums })
    else:
        searches = request.POST['searches']

        if searches:
            continent = Continent.objects.get(name = search)
            p = Paginator(Recipe.objects.filter( Q(continent_id = continent) & Q(name__icontains = searches) | Q(price__icontains = searches) ).order_by('-id'), 20)
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
                return render(request, "userrecipe/recipe_result.html",  { "recipes" : recipes_ratings, "message" : search, 'nums' : nums })
            
            else:
                return render(request, "userrecipe/recipe_result.html", { "recipes" : recipes_ratings, "message" : search, 'nums' : nums })



def GetRecipe(request):
    p = Paginator(Recipe.objects.all().order_by('-id'), 2)
    page = request.GET.get('page')
    recipes = p.get_page(page)
    nums = "a" * recipes.paginator.num_pages
    recipes_ratings = []

    for recipe_obj in recipes:
        recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.id)
        total_rating = CalculateRating(recipe_rating_obj) + 1
        response = {
            "recipe" : recipe_obj,
            "rating" : range(total_rating),
        }
        recipes_ratings.append(response)
    return render(request,"userrecipe/get_recipe.html",  { "recipes":recipes_ratings, 'nums':nums })



def GetRecipeById(request, recipe_id):
    recipe = Recipe.objects.get(id = recipe_id)
    recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe.id)
    total_rating = CalculateRating(recipe_rating_obj) + 1
    regularuser = RegularUser.objects.get(admin = request.user.id)
    favorite = RecipeFavorite.objects.filter(recipe_id = recipe, regularuser_id = regularuser)

    response = {
        "recipe" : recipe,
        "rating" : total_rating,
    }
        
    return render(request, "userrecipe/get_recipe_id.html",  { "recipe" : response, "favorite" : favorite })



def GetRecipeFeedBack(request, recipe_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    if request.method == 'POST':
        #message = request.POST['message']
        recipe_obj = Recipe.objects.get(id = recipe_id)

        new_commentary = RecipeCommentary.objects.create(
            #message = message,
            regularuser_id = user_obj,
            recipe_id = recipe_obj,
            show_comment = True
        )

        return HttpResponseRedirect(reverse("get_user_recipe_feedback", kwargs = { "recipe_id":recipe_id }))
    else:
        recipe = Recipe.objects.get(id = recipe_id)

        recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe.id)

        p = Paginator(RecipeCommentary.objects.filter(recipe_id = recipe_id).order_by('-created_at'), 5)
        page = request.GET.get('page')
        recipeCommentary = p.get_page(page)
        nums = "a" * recipeCommentary.paginator.num_pages

        total_rating = CalculateRating(recipe_rating_obj) + 1

        rating = RecipeRating.objects.filter(recipe_id = recipe, regularuser_id = user_obj).exists()
        if(rating):
           rating_exist = RecipeRating.objects.get(recipe_id = recipe, regularuser_id = user_obj).rating
        else:
            rating_exist = 0

        response = {
            "recipe" : recipe,
            "rating" : range(total_rating),
            "ratingCount" : total_rating,
            "count" : recipe_rating_obj.count()
        }
            
        return render(request, "userrecipe/recipe_feedback.html",  { "recipe" : response, "commentary" : recipeCommentary, 'nums' : nums,  "rating" : rating_exist  })



def GeteRecipeById(request, recipe_id):
    if request.method == 'POST':
        rating = request.POST['rating']
        user_obj = RegularUser.objects.get(admin = request.user.id)
        recipe_obj = Recipe.objects.get(id = recipe_id)
        recipeRating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj, regularuser_id = user_obj).exists()

        if(recipeRating_obj):
            recipeRating_obj = RecipeRating.objects.get(recipe_id = recipe_obj, regularuser_id = user_obj)
            recipeRating_obj.rating = rating
            recipeRating_obj.save()
        
        else:
            new_Rating = RecipeRating(
                rating = rating,
                regularuser_id = user_obj,
                recipe_id = recipe_obj
            )

            new_Rating.save()

        return JsonResponse({'success':'true', 'score': rating}, safe=False)

 
def GetChefById(request, chef_id):
    chefuser = ChefUser.objects.get(id = chef_id)
    recipe = Recipe.objects.filter(chefuser_id = chefuser).order_by('-created_at')
    regularuser = RegularUser.objects.get(admin = request.user.id)
    favorite = RegularUserFavorite.objects.filter(chefuser_id = chefuser, regularuser_id = regularuser)
    p = Paginator(recipe, 5)
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
    return render(request, "userrecipe/chef.html",  { "recipes" : recipes_ratings, "chef" : chefuser, 'nums' : nums, "recipe_count" : recipe.count(), "favorite" : favorite })



def ChefResult(request, search):
    if request.method != "POST":
        continent = Continent.objects.get(name = search)
        p = Paginator(ChefUser.objects.filter(continent_id = continent).order_by('?'), 20)
        page = request.GET.get('page')
        chefs = p.get_page(page)
        nums = "a" * chefs.paginator.num_pages

        return render(request, "userrecipe/chef_result.html",  { "chefs" : chefs, "message" : search, 'nums':nums })

    else: 
        searches = request.POST['searches']

        if searches:
            continent = Continent.objects.get(name = search)
            p = Paginator(ChefUser.objects.filter( Q(continent_id = continent) & Q(chef_name__icontains = searches) ).order_by('-id'), 20)
            page = request.GET.get('page')
            chefs = p.get_page(page)
            nums = "a" * chefs.paginator.num_pages

            if chefs:
                return render(request, "userrecipe/chef_result.html",  { "chefs" : chefs, "message" : search, 'nums':nums })
            
            else:
                return render(request, "userrecipe/chef_result.html", { "chefs" : chefs, "message" : search, 'nums':nums })


def GetRecipeFavorite(request):
    user_obj = RegularUser.objects.get(admin = request.user.id)

    p = Paginator(RecipeFavorite.objects.filter(regularuser_id = user_obj).order_by('?'), 20)
    page = request.GET.get('page')
    recipes = p.get_page(page)
    nums = "a" * recipes.paginator.num_pages
    recipes_ratings = []

    for recipe_obj in recipes:
        recipe_rating_obj = RecipeRating.objects.filter(recipe_id = recipe_obj.recipe_id.id)
        total_rating = CalculateRating(recipe_rating_obj) + 1
        response = {
            "recipe" : recipe_obj.recipe_id,
            "rating" : total_rating,
        }
        recipes_ratings.append(response)

    return render(request, "userrecipe/recipe_favorite.html",  { "recipes" : recipes_ratings, 'nums' : nums })



def CreateRecipeFavorite(request, recipe_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    recipe_obj = Recipe.objects.get(id = recipe_id)
   
    favorite = RecipeFavorite.objects.create(
        regularuser_id = user_obj,
        recipe_id = recipe_obj
    )

    return HttpResponseRedirect(reverse("user_recipe_id", kwargs = { "recipe_id":recipe_id }))


def DeleteRecipeFavorite(request, recipe_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    recipe_obj = Recipe.objects.get(id = recipe_id)
    favorite = RecipeFavorite.objects.get(recipe_id = recipe_obj , regularuser_id = user_obj)

    favorite.delete()

    return HttpResponseRedirect(reverse("user_recipe_id", kwargs = { "recipe_id":recipe_id }))
 

def GetRegularUserFavorite(request):
    user_obj = RegularUser.objects.get(admin = request.user.id)

    chef = Paginator(RegularUserFavorite.objects.filter(regularuser_id = user_obj).order_by('?'), 20)
    page = request.GET.get('page')
    chefusers = chef.get_page(page)
    nums = "a" * chefusers.paginator.num_pages

    return render(request, "userrecipe/regularuser_favorite.html",  { "chefs" : chefusers , 'nums' : nums })


def CreateRegularUserFavorite(request, chef_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    chefuser = ChefUser.objects.get(id = chef_id)
   
    favorite = RegularUserFavorite.objects.create(
        regularuser_id = user_obj,
        chefuser_id = chefuser
    )

    return HttpResponseRedirect(reverse("chef_recipe_id", kwargs = { "chef_id": chef_id }))


def DeleteRegularUserFavorite(request, chef_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    chefuser = ChefUser.objects.get(id = chef_id)

    favorite = RegularUserFavorite.objects.get(chefuser_id = chefuser , regularuser_id = user_obj)

    favorite.delete()

    return HttpResponseRedirect(reverse("chef_recipe_id", kwargs = { "chef_id": chef_id }))




#Book appointment
def GetBookingPending(request):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.filter(regularuser_id = regularuser, approved = False).order_by('-created_at')

    p = Paginator(appointment, 20)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    return render(request, "userrecipe/booking_pending.html", { "appointments" : appointments, 'nums' : nums })


def GetBookingResponse(request):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.filter(regularuser_id = regularuser, approved = True).order_by('-created_at')

    p = Paginator(appointment, 20)
    page = request.GET.get('page')
    appointments = p.get_page(page)
    nums = "a" * appointments.paginator.num_pages

    return render(request, "userrecipe/booking_approve.html", { "appointments" : appointments, 'nums' : nums })



def RecipeBookingConfirmation(request, appointment_id):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.get(id = appointment_id, regularuser_id = regularuser)

    return render(request, "userrecipe/recipe_booking_confirmation.html", { "appointment" : appointment })


def CreateRecipeBooking(request, recipe_id):
    if request.method!="POST":
        form = CreateAppointmentForm()
        recipe = Recipe.objects.get(id = recipe_id)
        return render(request, "userrecipe/recipe_create_booking.html", { "form": form, "recipe" : recipe })
    else:
        form = CreateAppointmentForm(request.POST,request.FILES)

        if form.is_valid():
            booking_time = form.cleaned_data["booking_time"]
            booking_date = form.cleaned_data["booking_date"]
            quantity = form.cleaned_data["quantity"]
            address = form.cleaned_data["address"]

            try:
                regularuser = RegularUser.objects.get(admin = request.user.id)
                recipe = Recipe.objects.get(id = recipe_id)

                appointment = Appointment.objects.create(
                    booking_time = booking_time,
                    booking_date = booking_date,
                    quantity = quantity,
                    address = address,
                    recipe_id = recipe,
                    regularuser_id = regularuser,
                    chefuser_id = recipe.chefuser_id
                )

                messages.success(request,"Successfully create an appointment")
                return HttpResponseRedirect(reverse("recipe_booking_confirmation", kwargs = { "appointment_id": appointment.id }))

            except:
                messages.error(request,"Failed to create an appointment")
                return HttpResponseRedirect(reverse("recipe_create_booking"), kwargs = { "recipe_id": recipe_id })

        else:
            form = CreateAppointmentForm()
            return render(request, "userrecipe/recipe_create_booking.html", { "form": form })


def EditRecipeBooking(request, appointment_id):
    if request.method!="POST":
        regularuser = RegularUser.objects.get(admin = request.user.id)
        appointment = Appointment.objects.get(id = appointment_id , regularuser_id = regularuser)       
        form = EditAppointmentForm()
        form.fields['booking_time'].initial = appointment.booking_time
        form.fields['booking_date'].initial = appointment.booking_date
        form.fields['quantity'].initial = appointment.quantity
        form.fields['address'].initial = appointment.address        
        return render(request, "userrecipe/recipe_edit_booking.html", { "form": form, "appointment" : appointment })
    else:
        form = EditAppointmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            booking_time = form.cleaned_data["booking_time"]
            booking_date = form.cleaned_data["booking_date"]
            quantity = form.cleaned_data["quantity"]
            address = form.cleaned_data["address"]

            try:
                regularuser = RegularUser.objects.get(admin = request.user.id)
                appointment = Appointment.objects.get(id = appointment_id , regularuser_id = regularuser)

                appointment.booking_time = booking_time
                appointment.booking_date = booking_date
                appointment.quantity = quantity
                appointment.address = address
                appointment.created_at = datetime.now()
                appointment.approved = False
                appointment.message = "Pending"

                appointment.save()

                messages.success(request,"Successfully Edit an appointment")
                return HttpResponseRedirect(reverse("recipe_booking_confirmation", kwargs = { "appointment_id": appointment.id }))

            except:
                messages.error(request,"Failed to Edit an appointment")
                return HttpResponseRedirect(reverse("recipe_booking_confirmation"))

        else:
            form = EditAppointmentForm()
            return render(request, "userrecipe/recipe_edit_booking.html", { "form": form })


def DeleteRecipeBooking(request, appointment_id):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    appointment = Appointment.objects.get(id = appointment_id, regularuser_id = regularuser)

    appointment.delete()
    messages.error(request,"Delete Appointment")
    return HttpResponseRedirect(reverse("booking_pending"))



def RecipeCountriesResult(request, search):
    if request.method != "POST":

        country = Country.objects.get(name = search)
        countries = Country.objects.all().order_by('name')
        p = Paginator(Recipe.objects.filter(country_id = country).order_by('?'), 20)
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
        return render(request, "userrecipe/recipe_countries_result.html",  { "recipes" : recipes_ratings, "message" : search, 'nums' : nums, "countries" : countries })
    else:
        searches = request.POST['searches']

        prefer_country = request.POST['country']

        countries = Country.objects.all().order_by('name')

        if searches:
            country = Country.objects.get(name = prefer_country)
            p = Paginator(Recipe.objects.filter( Q(country_id = country) & Q(name__icontains = searches) | Q(price__icontains = searches) ).order_by('-id'), 20)
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
                return render(request, "userrecipe/recipe_countries_result.html",  { "recipes" : recipes_ratings, "message" : prefer_country, 'nums' : nums, "countries" : countries })
            
            else:
                return render(request, "userrecipe/recipe_countries_result.html", { "recipes" : recipes_ratings, "message" : prefer_country, 'nums' : nums, "countries" : countries })




## Payment
def GetAllPaymentBooking(request):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    payment = Payment.objects.filter(regularuser_id = regularuser, approved = True).order_by('-created_at')

    p = Paginator(payment, 20)
    page = request.GET.get('page')
    payments = p.get_page(page)
    nums = "a" * payments.paginator.num_pages

    return render(request, "userrecipe/get_all_payment.html.html", { "payments" : payments, 'nums' : nums })



def GetPaymentBooking(request, payment_id):
    regularuser = RegularUser.objects.get(admin = request.user.id)
    payment = Payment.objects.get(id = payment_id, regularuser_id = regularuser)

    return render(request, "userrecipe/get_payment.html", { "payment" : payment })


def CreatePaymentBooking(request, appointment_id):
    if request.method!="POST":
        form = CreatePaymentForm()
        regularuser = RegularUser.objects.get(admin = request.user.id)
        appointment = Appointment.objects.get(id = appointment_id , regularuser_id = regularuser, message = "Approved")       
     
        return render(request, "userrecipe/payment.html", {"appointment" : appointment, "form" : form })
    else:
        form = CreatePaymentForm(request.POST, request.FILES)
        
        if form.is_valid():
            card_number = form.cleaned_data["card_number"]
            cvv = form.cleaned_data["cvv"]
            pin = form.cleaned_data["pin"]

            try:
                regularuser = RegularUser.objects.get(admin = request.user.id)
                appointment_detail = Appointment.objects.get(id = appointment_id , regularuser_id = regularuser, message = "Approved")

                payment = Payment.objects.create(
                    booking_time = appointment_detail.booking_time,
                    booking_date = appointment_detail.booking_date,
                    quantity = appointment_detail.quantity,
                    address = appointment_detail.address,
                    recipe_id = appointment_detail.recipe_id,
                    regularuser_id = appointment_detail.regularuser_id,
                    chefuser_id = appointment_detail.chefuser_id
                )

                appointment_detail.delete()

                messages.success(request,"Successfully make payment")
                return HttpResponseRedirect(reverse("get_paymment_booking", kwargs = { "payment_id": payment.id }))

            except:
                messages.error(request,"Error in payment transaction")
                return HttpResponseRedirect(reverse("create_payment_booking"))

        else:
            form = CreatePaymentForm()
            return render(request, "userrecipe/payment.html", { "form": form })
