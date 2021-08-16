from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from chef_management_app.models import ChefUser, Continent, RecipeCommentary, Recipe, RecipeImages, RegularUser, RecipeRating, Country, RecipeFavorite, RegularUserFavorite



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
    return render(request, "userrecipe/recipe_result.html",  { "recipes" : recipes_ratings, "message" : search, 'nums':nums })



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
        #user_obj = RegularUser.objects.get(admin = request.user.id)
        #recipeImages = RecipeImages.objects.filter(recipe_id = recipe_id)
        #recipeCommentary = RecipeCommentary.objects.filter(recipe_id = recipe_id)
        #rating = RecipeRating.objects.filter(recipe_id = recipe, regularuser_id = user_obj).exists()
        #if(rating):
         #   rating_exist = RecipeRating.objects.get(recipe_id = recipe, regularuser_id = user_obj).rating
        #else:
         #   rating_exist = 0
        #return render(request, "userrecipe/get_recipe_id.html", { "recipe" : recipe, "recipeImages" : recipeImages, "commentary" : recipeCommentary, "rating" : rating_exist } )


def GetRecipeFeedBack(request, recipe_id):
    user_obj = RegularUser.objects.get(admin = request.user.id)
    if request.method == 'POST':
        message = request.POST['message']
        recipe_obj = Recipe.objects.get(id = recipe_id)

        new_commentary = RecipeCommentary.objects.create(
            message = message,
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
    continent = Continent.objects.get(name = search)
    p = Paginator(ChefUser.objects.filter(continent_id = continent).order_by('?'), 20)
    page = request.GET.get('page')
    chefs = p.get_page(page)
    nums = "a" * chefs.paginator.num_pages

    return render(request, "userrecipe/chef_result.html",  { "chefs" : chefs, "message" : search, 'nums':nums })


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