# We have added the necessary fields to our data base in our models.py
# Django will generate the forms automatically according to our model
# This is to style the django generated forms we used in add_post.html
from django import forms
from . models import Comment, Post, Category
# Defining a new variable to add dropdown menus for our 'category' select menu.
#choices = [('coding', 'coding'), ('sports','sports'),('entertainment','entertainment')]
# Not using the above method since it is not dynamic
# The next method involves importing the Category model from models.py
# Making lists dynamic
choices= Category.objects.all().values_list('name','name')
# Using 'name' here since in our Category model we used 'name' 
# Next we want to loop through the entire category list, for that we need to use a for loop
# Declaring a new variable to use it in the for loop
choice_list = []
for item in choices:
    choice_list.append(item)
# Next we need to set choices = choice_list

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','title_tag', 'author','category', 'body', 'snippet', 'header_image')
        # To style the forms we use widgets
        # Here we pass the styling as attributes in a dictionary
        # We are using bootstrap classes here
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            # To make sure a particular user can make posts only as their own behalf and not as a different user by selecting a diffrerent users name on add post page, changing 'author' field from a drop down to a text field and we hide the text field using 'type':'hidden' attribute.
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'id': 'user', 'value':'', 'type': 'hidden'}),

            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'body': forms.Textarea(attrs={'class':'form-control'}),
        }