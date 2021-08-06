from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from chef_management_app.models import RecipeCommentary, Recipe, RecipeImages, RegularUser, RecipeRating



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
    if request.method == 'POST':
        message = request.POST['message']
        user_obj = RegularUser.objects.get(admin = request.user.id)
        recipe_obj = Recipe.objects.get(id = recipe_id)

        new_commentary = RecipeCommentary(
            message = message,
            regularuser_id = user_obj,
            recipe_id = recipe_obj,
            show_comment = True
        )

        new_commentary.save()

        response = {
            "message" : message,
            "created" : "Now",
        }

        return JsonResponse(response)
    else:
        recipe = Recipe.objects.get(id = recipe_id)
        user_obj = RegularUser.objects.get(admin = request.user.id)
        recipeImages = RecipeImages.objects.filter(recipe_id = recipe_id)
        recipeCommentary = RecipeCommentary.objects.filter(recipe_id = recipe_id)
        rating = RecipeRating.objects.filter(recipe_id = recipe, regularuser_id = user_obj).exists()
        if(rating):
            rating_exist = RecipeRating.objects.get(recipe_id = recipe, regularuser_id = user_obj).rating
        else:
            rating_exist = 0
        return render(request, "userrecipe/get_recipe_id.html", { "recipe" : recipe, "recipeImages" : recipeImages, "user" : user_obj.image_url, "commentary" : recipeCommentary, "rating" : rating_exist } )


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