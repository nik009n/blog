from django.shortcuts import render, get_object_or_404
# Importing get_object_or_404 to keep track of which post is getting the likes and who is pressing the like button
# Import ListView to display all the contents at once, it will look through the database and list out the data
# DetailView to display one partcular thing

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Import 'Post' model we created in models.py to use it here
from . models import Comment, Post, Category
from . forms import PostForm, CommentForm
# To redirect to a page once a post has been deleted 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
# Create your views here.

# def home(request):
#       return render(request, 'home.html', {})

# Creating a functon view to make a like button in our posts
def LikeView(request,pk):
    # Creating a variable
    # Here id=request.POST.get('post_id') since we are submitting a form in our article_deatils.html we can grab something from that form and assign as the id, post_id is the name we have given the form in our article deatils page.
    # Now we can use this id to look through our 'Post' table in our model
    # Then assigning all that to a new variable
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    # Now we need to save this 'post' variable to our table
    # Here we use 'request.user' since we also need to know who has liked the post
    # To create an unlike button we have to first create a variable and set it False
    liked = False
    # Creating an if statement to make sure a user can only like a post once and unlike it if they click on it again.
    # Here 'post' is the variable we store the id of the user.
    # Here 'likes' is the name of field in 'Post' model.
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    
    # Now after liking a post we need the user to stay on the same page, for this we need to import HttpResponseRedirect and reverse.
    # Then we pass in the name of the page and 'pk' which we have passed as an argument in the function.
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))
    # Next create a function to count the total number of likes a post gets in the 'Post' model in models.py


# Using a class view here and passing the argument 'ListView' instead of 'request'
class HomeView(ListView):
    model = Post 
    # Post is the model we created earlier
    template_name = 'home.html'
    # To order the post from latest to old
    # 'id' is the primary key django generates and '-' sign makes sure it is sorted latest to old
    #ordering = ['-id']
    # To order by date
    ordering = ['-post_date']
# Next go to 'home.html' to type the code to fetch the data from the database
    # To write query to fetch our category pages directly
    def get_context_data(self, *args, **kwargs):
        # We want to query our Category model in our database and pull out all the categories to generate links which then we can use in our drop down to link to the different category pages
        # Now define a variable to put the things in our Category model, but since it only has one thing 'name' we dont't need to filter the data.
        cat_menu = Category.objects.all
        # Now to push this cat_menu variable on the page as a context dictionary
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        # We can turn this context variable into a context_dictionary
        context["cat_menu"] = cat_menu
        return context

def CategoryListView(request):
    # To query the database and make a list of all the categories.
    cat_menu_list = Category.objects.all
    # Now we pass this cat_menu_list variable as a context dictionary to create a link to each category
    return render(request, 'category_list.html',{ 'cat_menu_list': cat_menu_list})

# Defining a function view to create a page where we can see all the posts from one category
def CategoryView(request, cats):
    # Since we have assigned 'category/<str:cats>/' in urls.py
    # This allows when we pass in the request we can pass this as the url to get desired category directly
    # Next write a query to fetch data from the data base
    # Class based views do this automatically
    # Here 'category_posts' is a new variable to store the filtered data
    # We set 'category=cats' since we defined 'category' as the field name in our model
    # Here 'cats' is the argument we pass in through the url
    # category=cats will look for the category that we pass in through the url.
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html',{'cats': cats.replace('-',' '), 'category_posts': category_posts})
    # We can use {'cats': cats, 'category_posts': category_posts} in our categories.html to display content dynamically
    # Here we add category=cats.replace('-', ' ') since we slugify the url, when sending a request the page will send the url with a '-', so we need to replace the '-' with white spaces, because when we query our database since we didn't create the categories with '-' it will not match and we wouldn't get the desired page.
    # We also add 'cats':cats.replace('-',' ') so that when we use {{ cats }} code it will also replace the '-' with white space.

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    # Here we add the same function used in the HomeView to add the Category dropdown in the aricle_details page
    def get_context_data(self, *args, **kwargs):
        # We want to query our Category model in our database and pull out all the categories to generate links which then we can use in our drop down to link to the different category pages
        # Now define a variable to put the things in our Category model, but since it only has one thing 'name' we dont't need to filter the data.
        cat_menu = Category.objects.all
        # Now to push this cat_menu variable on the page as a context dictionary
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        # We can turn this context variable into a context_dictionary
        context["cat_menu"] = cat_menu
        
        # Creating a variable to get the id of the post getting the likes
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        # Creating a variable to pass in the total likes using the total_likes function defined views.py, then using the 'stuff' variable to get the total no of likes of a particular post because we pass in 'pk' as an argument.
        total_likes = stuff.total_likes()
        # Creating an if statement to make sure a user can only like a post once.
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        # Creating a context  variable to pass the total no of likes
        context["total_likes"] = total_likes
        context["liked"] = liked
        # Now go to article_deatils.html to pass in the number of likes dynamically.
        return context

# To make a page where we can make new blog posts and add it to the data base
class AddPostView(CreateView):
    model = Post
    # PostForm is the class we defined in forms.py
    form_class = PostForm
    template_name = 'add_post.html'

# To add a comment section where users can post comments using the blog page.
class AddCommentView(CreateView):
    model = Comment
    # PostForm is the class we defined in forms.py
    form_class = CommentForm
    template_name = 'add_comment.html'
    # fields = '__all__'
    success_url = reverse_lazy('home')
    # To get the id of the post that we add the comment on.
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
# To create new categories from a webpage rather than the admin section 
class AddCategoryView(CreateView):
    model = Category
    # Category is the new model we defined in models.py
    #form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'
    
class UpdatePostView(UpdateView):
    model = Post
    # To style the page using the bootstrap template we used earlier
    form_class = PostForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']
    
# To delete a blog post from the webpage
class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'    
    # To redirect to a page after the post is deleted we need to provide a success_url
    success_url = reverse_lazy('home') 