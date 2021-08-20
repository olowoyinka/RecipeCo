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
    path('chef/dashboard', chefView.HomePages, name="chef_home"),
    path('chef/register', homeView.ChefRegister, name="chef_register"),
    path('chef/edit', chefView.EditChef, name="edit_chef"),
    path('chef/image', chefView.ImageChef, name="chef_image"),
    path('chef/image/remove', chefView.RemoveImageChef, name="remove_chef_image"),
    path('chef/feature_image', chefView.FeatureImageChef, name="feature_chef_image"),
    path('chef/feature_image/<str:chef_image_id>/remove', chefView.RemoveFeatureImageChef, name="remove_feature_chef_image"),

    #User
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
    path('chef/recipe/<str:recipe_id>/feedback', recipeView.GetRecipeFeedBack, name="get_recipe_feedback"),
    path('chef/recipe/edit/<str:recipe_id>', recipeView.EditRecipe, name="edit_recipe"),
    path('chef/recipe/delete/<str:recipe_id>', recipeView.DeleteRecipe, name="delete_recipe"),
    path('chef/recipe/feature_image/<str:recipe_id>', recipeView.FeatureRecipeImage, name="feature_recipe_image"),
    path('chef/recipe/feature_image/<str:recipe_image_id>/remove', recipeView.DeleteFeatureRecipeImage, name="remove_feature_recipe_image"),

    #Chef_Booking
    path('chef/booking/pending', recipeView.GetBookingPending, name="chef_booking_pending"),
    path('chef/booking/approved', recipeView.GetBookingResponse, name="chef_booking_approved"),
    path('chef/booking/payment', recipeView.GetBookingPayment, name="chef_booking_payment"),

    path('chef/booking/<str:appointment_id>/confirmation', recipeView.RecipeBookingConfirmation, name="chef_booking_confirmation"),
    path('chef/booking/<str:appointment_id>/confirmation_approved', recipeView.BookingApproved, name="chef_booking_confirmation_approved"),
    path('chef/booking/<str:appointment_id>/confirmation_declined', recipeView.BookingDeclined, name="chef_booking_confirmation_declined"),

    #User_Recipe
    path('dashboard', userRecipeView.HomePage, name="user_home"),
    path('recipe', userRecipeView.GetRecipe, name="user_recipe"),
    path('chef/<str:chef_id>', userRecipeView.GetChefById, name="chef_recipe_id"),
    path('favorite/chef', userRecipeView.GetRegularUserFavorite, name="get_chef_favorite"),
    path('chef/<str:chef_id>/favorite', userRecipeView.CreateRegularUserFavorite, name="chef_favorite"),
    path('chef/<str:chef_id>/remove_favorite', userRecipeView.DeleteRegularUserFavorite, name="chef_remove_favorite"),
    path('recipe/<str:recipe_id>', userRecipeView.GetRecipeById, name="user_recipe_id"),
    path('favorite/recipe', userRecipeView.GetRecipeFavorite, name="get_recipe_favorite"),
    path('recipe/<str:recipe_id>/favorite', userRecipeView.CreateRecipeFavorite, name="user_recipe_favorite"),
    path('recipe/<str:recipe_id>/remove_favorite', userRecipeView.DeleteRecipeFavorite, name="user_recipe_remove_favorite"),
    path('recipe/<str:recipe_id>/feedback', userRecipeView.GetRecipeFeedBack, name="get_user_recipe_feedback"),
    path('recipe/search/<str:search>', userRecipeView.RecipeResult, name="user_recipe_search"),
    path('chef/search/<str:search>', userRecipeView.ChefResult, name="user_chef_search"),
    path('recipe_rating/<str:recipe_id>', userRecipeView.GeteRecipeById, name="recipe_rating_id"),

 
    #Recipe_Booking
    path('recipe/<str:recipe_id>/booking', userRecipeView.CreateRecipeBooking, name="recipe_create_booking"),
    path('booking/<str:appointment_id>/edit', userRecipeView.EditRecipeBooking, name="recipe_edit_booking"),
    path('booking/<str:appointment_id>/delete', userRecipeView.DeleteRecipeBooking, name="recipe_delete_booking"),
    path('booking/<str:appointment_id>/confirmation', userRecipeView.RecipeBookingConfirmation, name="recipe_booking_confirmation"),
    path('booking', userRecipeView.GetBookingPending, name="booking_pending"),
    path('booking/response', userRecipeView.GetBookingResponse, name="booking_response"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)