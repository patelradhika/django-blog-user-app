from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UserForm, LoginForm
from .models import BlogPost


# Create your views here.
ALLOWED_SPECIAL_CHAR = ['_', '@', '$', '#']


def home(request):
    blogs = BlogPost.objects.filter(posted_on__lte=timezone.now()).order_by('-posted_on')
    paginator = Paginator(blogs, 2)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    if not page_num or int(page_num) <= paginator.num_pages:
        frontend = {'blogs': blogs, 'page': page}
        return render(request, 'blog/home.html', frontend)
    
    else:
        return render(request, 'error/404.html')


def about(request):
    return render(request, 'blog/about.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            check = form.cleaned_data['check_password']

            if User.objects.filter(email=email):
                form.errors['email'] = ["Email ID already registered with us."]

            elif password != check:
                form.errors['password'] = ["Passwords must match."]

            elif len(password) < 8                                                          \
            or not any(char.isdigit() for char in password)                                 \
            or not any(char.isupper() for char in password)                                 \
            or not any(char.islower() for char in password)                                 \
            or not any(not char.isalnum() for char in password)                             \
            or not any(char in ALLOWED_SPECIAL_CHAR for char in password):
                form.errors['password'] = ["Password does not match criteria."]

            else:
                new_user = User.objects.create_user(username, email, password)
                return redirect('/')

    else:
        form = UserForm()

    frontend = {'form': form}
    return render(request, 'blog/register.html', frontend)


def cust_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)

            except ObjectDoesNotExist:
                form.errors['username'] = ["Username not registered with us."]

            else:
                if not user.check_password(password):
                    form.errors['password'] = ["Incorrect password entered."]

                else:
                    login(request, user)
                    return redirect('/')
    
    else:
        form = LoginForm()

    frontend = {'form': form}
    return render(request, 'blog/login.html', frontend)


def cust_logout(request):
    logout(request)
    return redirect('/')