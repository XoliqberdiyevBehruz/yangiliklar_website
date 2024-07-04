from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.generic import ListView
from news_app.models import News
from django.db.models import Q 
# Create your views here.
@login_required
def dashboard_view(request):
    user = request.user
    context = {
        "user":user
    }
    return render(request, 'pages/user_profile.html', context=context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user":new_user
            }
            return render(request, 'account/register_done.html', context)
        
    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'account/register.html', {"user_form":user_form})

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_edit = UserEditForm(instance=request.user, data=request.POST)
        profile_edit = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_edit.is_valid() and profile_edit.is_valid():
            profile_edit.save()
            user_edit.save()

    else:
        user_edit = UserEditForm(instance=request.user)
        profile_edit = ProfileEditForm(instance=request.user)
     
    
    return render(request, 'account/profile_edit.html', {"user_edit":user_edit, 'profile_edit':profile_edit})


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    users = User.objects.all()
    context = {
        'admin_users':admin_users,
        'users':users,
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query)|Q(body__icontains=query))