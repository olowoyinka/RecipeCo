import datetime
import os
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
  
from ckeditor.fields import RichTextField


#file path
def filepath_chef(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('chef/', filename)

def filepath_chef_image(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('chef_images/', filename)

def filepath_user(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('user/', filename)

def filepath_recipe(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('recipe/', filename)

def filepath_recipe_image(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('recipe_images/', filename)


# Create your models here.

class Continent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    objects = models.Manager()


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    continent_id = models.ForeignKey(Continent, on_delete=models.CASCADE)
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Chef"),(3,"Regular"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class ChefUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    chef_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to=filepath_chef,null=True,blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    address_name = models.TextField()
    country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True,blank=True)
    continent_id = models.ForeignKey(Continent, on_delete=models.DO_NOTHING, null=True,blank=True)
    objects = models.Manager()


class RegularUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=filepath_user,null=True,blank=True)
    phone_number = models.CharField(max_length=255)
    join_date = models.DateTimeField(auto_now_add=True)
    country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True,blank=True)
    continent_id = models.ForeignKey(Continent, on_delete=models.DO_NOTHING, null=True,blank=True)
    objects = models.Manager()


class RegularUserFavorite(models.Model):
    id = models.AutoField(primary_key=True)
    chefuser_id = models.ForeignKey(ChefUser, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    objects = models.Manager()


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    decription = RichTextField(blank=True,null=True)
    method = RichTextField(blank=True,null=True)
    ingredient = RichTextField(blank=True,null=True)
    image_url = models.ImageField(upload_to=filepath_recipe,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    period = models.IntegerField()
    address_name = models.TextField()
    country_id = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True,blank=True)
    continent_id = models.ForeignKey(Continent, on_delete=models.DO_NOTHING, null=True,blank=True)
    chefuser_id = models.ForeignKey(ChefUser, on_delete=models.CASCADE)
    objects = models.Manager()


class RecipeFavorite(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    objects = models.Manager()


class ChefImages(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ImageField(upload_to=filepath_chef_image,null=False,blank=False)
    chefuser_id = models.ForeignKey(ChefUser, on_delete=models.CASCADE)
    objects = models.Manager()


class RecipeCommentary(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    show_comment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    objects = models.Manager()


class RecipeImages(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.ImageField(upload_to=filepath_recipe_image,null=False,blank=False)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    objects = models.Manager()


class RecipeRating(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default=0, 
        validators = [
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    objects = models.Manager()


class RecipeSurvey(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.TextField()
    objects = models.Manager()


class RecipeRecordSurvey(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=255)
    recipesurvey_id = models.ForeignKey(RecipeSurvey, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    booking_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    chefuser_id = models.ForeignKey(ChefUser, on_delete=models.CASCADE)
    regularuser_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE)
    objects = models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            ChefUser.objects.create(admin=instance)
        if instance.user_type==3:
            RegularUser.objects.create(admin=instance)


@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.chefuser.save()
    if instance.user_type==3:
        instance.regularuser.save()