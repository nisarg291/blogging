from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
#this is required bcz Post is required relationship with author
#one post have only one user
#but one user can have mulitple post so we requeired and User is super user which are we created
# for show how many users are their User.objects.all() here nisarg,nisarg2,nisargblog
#for shw the sql command python3 manage.py sqlmigrate blog(app. name) 0001 for showing sql command for creating table when we call the command python3 manage.py migrate it call this sql command automatically
#python3 manage.py startapp appname for staring application in project directory ni under aa command karvanu bcz always app is created inside project
#django-admin startproject projectname for starting project

#each class is the table in database 
#each attr is column of the table
class Post(models.Model):
    title = models.CharField(max_length=50)
    head0 = models.CharField(max_length=500, default="")
    chead0 = models.CharField(max_length=5000, default="")
    head1 = models.CharField(max_length=500, default="")
    chead1 = models.CharField(max_length=5000, default="")
    head2 = models.CharField(max_length=500, default="")
    chead2 = models.CharField(max_length=5000, default="")
    pub_date = models.DateField(default=timezone.now)
    thumbnail = models.FileField(default="default.jpg",upload_to='blog/images')
    video=models.FileField(default="Default.mp4",upload_to="blog/video")
    content=models.CharField(max_length=10000,default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # this is the foreinkey with user class(table)
    #for that primary key of the user class is the foreignkey of post class
    #ondelete=models.CASCADE means if user is deleted then all post of that user is deleted

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    # we can also use redirect in views.py in createPostView method
    # def save(self):
    #     img=Image.open(self.thumbnail.path)
    #     if img.height>300 or img.width>300:
    #         output_size=(300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.thumbnail.path)