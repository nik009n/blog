from django.urls import path,include
# from . import views

# Import the class views we created in views.py
from . views import AddCommentView, HomeView, ArticleDetailView,AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView,LikeView


urlpatterns = [
    #path('', views.home, name="home"),
    #Here 'name' is the one we use to link to the page in the html file
    path('', HomeView.as_view(), name="home"),
    # Using "as_view" here since we use class view
    # Here 'name' is the thing we use to link to the particular page using Jinja format.
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail' ),
    # Here <int:pk> is the primary key django creates in the backend
    path('add_post/', AddPostView.as_view(), name='add_post'),
    # This is the page to create new blog posts
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    # To delete a blog post from the blog
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('category_list/', CategoryListView, name='category-list'),
    # For creating a like button
    path('like/<int:pk>', LikeView, name = 'like_post'),
    # To add a comment
    path('article/<int:pk>/comment>', AddCommentView.as_view(), name = 'add_comment'),

]
