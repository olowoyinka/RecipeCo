"""chef_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
#from chef_management_app import views
from chef_management_app.views import homeView
from chef_management_app.views import adminView
from chef_management_app.views import chefView
from chef_management_app.views import recipeView
from chef_management_app.views import regularUserView
from chef_management_app.views import userRecipeView
from chef_management import settings


urlpatterns = [
    
    path('', homeView.HomePage, name="home"),
    path('admin/', admin.site.urls),

    #Login
    path('login', homeView.Login, name="login"),
    path('logout', homeView.LogOut, name="logout"),
    path('activate-user/<uidb64>/<token>', homeView.activate_user, name="activate"),

    #Admin
    path('admin', adminView.HomePage, name="admin_home"),
 
    #Chef
    path('chef', chefView.HomePage, name="chef_home"),
    path('chef/register', homeView.ChefRegister, name="chef_register"),
    path('chef/edit', chefView.EditChef, name="edit_chef"),
    path('chef/image', chefView.ImageChef, name="chef_image"),
    path('chef/image/remove', chefView.RemoveImageChef, name="remove_chef_image"),
    path('chef/feature_image', chefView.FeatureImageChef, name="feature_chef_image"),
    path('chef/feature_image/<str:chef_image_id>/remove', chefView.RemoveFeatureImageChef, name="remove_feature_chef_image"),

    #User
    path('user_home', regularUserView.HomePage, name="user_home"),
    path('user/register', homeView.RegularUserRegister, name="user_register"),
    path('user/edit', regularUserView.EditRegularUser, name="edit_user"),
    path('user/image', regularUserView.ImageRegularUser, name="user_image"),
    path('user/image/remove', regularUserView.RemoveImageRegularUser, name="remove_user_image"),
    path('check_email_exist', homeView.check_email_exist, name="check_email_exist"),
    path('check_username_exist', homeView.check_username_exist, name="check_username_exist"),


    #Recipe
    path('chef/recipe/create', recipeView.CreateRecipe, name="create_recipe"),
    path('chef/recipe', recipeView.GetRecipe, name="get_recipe"),
    path('chef/recipe/<str:recipe_id>', recipeView.GetRecipeById, name="get_recipe_Id"),
    path('chef/recipe/edit/<str:recipe_id>', recipeView.EditRecipe, name="edit_recipe"),
    path('chef/recipe/delete/<str:recipe_id>', recipeView.DeleteRecipe, name="delete_recipe"),
    path('chef/recipe/feature_image/<str:recipe_id>', recipeView.FeatureRecipeImage, name="feature_recipe_image"),
    path('chef/recipe/feature_image/<str:recipe_image_id>/remove', recipeView.DeleteFeatureRecipeImage, name="remove_feature_recipe_image"),

    #User_Recipe
    path('recipe', userRecipeView.GetRecipe, name="user_recipe"),
    path('recipe/<str:recipe_id>', userRecipeView.GetRecipeById, name="user_recipe_id"),
    path('recipe_rating/<str:recipe_id>', userRecipeView.GeteRecipeById, name="recipe_rating_id")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)