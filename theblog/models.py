from django.db import models
# To connect the superuser we created 
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from django.urls import reverse 
# Create your models here.
# To use django date time feature 
from datetime import datetime, date
# To add a rich text editor to our blog
from ckeditor.fields import RichTextField

# For the users to create new categories themselves rather than coding it in our 'Post' model we need to create a new model. We are doing this after setting up the basic blog features.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        # Here 'home' doesn't have a primary key so we don't pass that as an argument
        return reverse('home')
        
    # After creating a new model we need to register it in our admin.py file
# Creating a new class to customize the user profile page
# It is hard to customize the Edit Profile page of our blog since we used django            UserCreationForm, so to customize it we are creating a new model and associating with the built in User model.
class Profile(models.Model):
    # Creating a variable to one to one associate with the User model in our memebers app
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile")
    # Here we use null=True, blank=True so that it will not raise an error if kept it blank
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)
    
    # To display the name of the user in the admin section
    def __str__(self):
        return str(self.user)
    
    # To redirect to a page after a new post is created from the web page
    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    # Here we define a blog post model by the name "Post"
    title = models.CharField(max_length=255)
    # To add images
    # Here we set null=True, blank=True to create posts without images if it is needed.
    # Now we don't actually store images in our data bases we store them in cloud and reference the address here. Here we are setting up an images folder in our directory.
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    title_tag = models.CharField(max_length=255, default = "My blog")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # ForeighnKey is from the user we created
    # 'User' is a django generated model we can use it by connecting it
    # Here "on_delete=models.CASCADE" to delete all the posts of user once the user is deleted
    #body = models.TextField()
    # To add a rich text editor to our blog
    body = RichTextField(blank=True, null=True)
    # Now we have to add this 'ckeditor' app to our settings.py file.
    # To add the date to each blog post automatically 
    post_date = models.DateField(auto_now_add=True)
    # To add categories in our blog
    category = models.CharField(max_length=255, default='coding')
    # The default= coding assigns all the existing posts in 'coding' category
    # To add snippets of the blog posts 
    snippet = models.CharField(max_length=255)
    # To add a like button we need to create a field in the database
    likes = models.ManyToManyField(User, related_name='blog_posts')
    # Here we use ManyToManyField as the type, since a like button can have as many likes as possible
    # Here we are associating django 'User' form by passing as an argument
    
    # Creating a funcion to count the total no of likes a post gets 
    def total_likes(self):
        return self.likes.count()
        
    
    def __str__(self):
        #To display the name of the user on the admin page 
        return self.title + ' | ' + str(self.author)
# Next goto views.py to create class views to make use of the model we created here
    # To redirect to a page after a new post is created from the web page
    def get_absolute_url(self):
        # We are passing arguments self.id which is the same primary key django generates
        return reverse('article-detail', args=[str(self.id)])

# To add a comment section to the blog
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
