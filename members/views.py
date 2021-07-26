from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from . forms import ProfilePageForm, SignUpForm, EditProfileForm, PasswordChangingForm
from django.urls import reverse_lazy
# Here we are using 'theblog.models' to import the Profile model since the model is in the theblog app instead of members app.
from theblog.models import Profile

# Create your views here.
class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "registration/create_user_profile_page.html"
    
    # To get the id of the user creating the profile page
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Creating a view to edit the user's profile, we already have an edit profile page with basic functionality now we create another one to change profile picture, social media links etc.
class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    # Naming the form fields we want to include in the form in the edit_profile page.
    fields = ['user', 'bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url','instagram_url', 'pinterest_url']
    # To redirect to a page after editing the profile
    success_url = reverse_lazy('home')



class ShowProfilePageView(DetailView):
    # Here Profile is the name of our model created in models.py. 
    model = Profile
    template_name = 'registration/user_profile.html'
    # Now we have to get the user's id that we used to reference individual users in our urls.py file, we have to create a function to get the context data since we are using a class view here.
    def get_context_data(self, *args, **kwargs):
        # We want to query our Profile model in our database and pull out the user id.
        # Now define a variable to put the things in our Profile model.
        #users = Profile.objects.all
        # Creating a new variable to get the id of the logged in user.
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        # Now to push this page_user variable on the page as a context dictionary
        context = super( ShowProfilePageView, self).get_context_data(*args, **kwargs)
        # We can turn this context variable into a context_dictionary
        context["page_user"] = page_user
        return context




# To redirect to a page after password is changed we are creating a new class view
# Here we inherit the PasswordChangeView
# Here PasswordChangeForm is a built in form 
class PasswordsChangeView(PasswordChangeView):
    #form_class = PasswordChangeForm
    # We have created a new form to style it.
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')

# To redirect to a new web page after the password change
def password_success(request):
    return render(request, 'registration/password_success.html',{})

class UserRegisterView(generic.CreateView):
    # UserCreationForm is a form built into django
    # In the other app we used "PostForm" class we created in forms.py 
    #form_class = UserCreationForm
    form_class = SignUpForm
    template_name = 'registration/register.html'
    # To redirect to a page after the registration 
    success_url = reverse_lazy('login')

# To edit the user profile
class UserEditView(generic.UpdateView):
    # UserChangeForm is a form built into django
    # EditProfileForm is a form we defined in forms.py to style our edit profile page.
    # In the other app we used "PostForm" class we created in forms.py 
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    # To redirect to a page after the registration 
    success_url = reverse_lazy('home')

    # To identify which user is logged in 
    def get_object(self):
        return self.request.user

