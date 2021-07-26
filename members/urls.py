from django.urls import path
from . views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, CreateProfilePageView
# To use the built in views to handle user authentication
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # Here 'password' is the url django uses
    # PasswordChageView is a built in view in django that we have imported here.
    # Here 'template_name' argument is used to style our password change page.
    #path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    # Here we can actually use the above url with built in PasswordChangeView to change our password, but in order to redirect it to a page after the password change we have defined a new view PasswordsChangeView in views.py file.
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    # To redirect to a new web page  after the password change, defining a new url here.
    path('password_success', views.password_success, name='password_success'),
    # Here we add the url of the user's profile page
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    # To createa a page where we can edit the user profile
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    # To make a page where users can create thier profiles 
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    
]
