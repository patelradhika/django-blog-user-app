from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from PIL import Image

from .forms import UserForm, LoginForm, AccountForm, BlogForm, CommentForm
from .models import BlogPost, UserImage, Comments


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
                UserImage.objects.create(user=new_user)
                messages.success(request, "Registration successful. Please login.")
                return redirect('login')

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
                    
                    if user.is_superuser:
                        return redirect('approvallist')
                    else:
                        return redirect('home')
    
    else:
        form = LoginForm()

    frontend = {'form': form}
    return render(request, 'blog/login.html', frontend)


def cust_logout(request):
    logout(request)
    return redirect('home')


@login_required
def useraccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            check = form.cleaned_data['check_pass']
            pic = form.cleaned_data['image']

            if email:
                if email == user.email:
                    form.errors['email'] = ['Email ID is already this.']

                elif User.objects.filter(email=email):
                    form.errors['email'] = ["Email ID already registered with us."]

                else:
                    user.email = email
                    user.save(update_fields=['email'])
                    messages.success(request, 'Email ID updated successfully.')
                    return redirect('useraccount')

            if username:
                if username == user.username:
                    form.errors['username'] = ["Username is already this."]

                elif User.objects.filter(username=username):
                    form.errors['username'] = ["A user with this username already exists."]

                else:
                    user.username = username
                    user.save(update_fields=['username'])
                    messages.success(request, "Username updated successfully.")
                    return redirect('useraccount')

            if password:
                if user.check_password(password):
                    form = AccountForm()
                    form.errors['password'] = ["New password cannot be same as current password."]

                elif not check:
                    form = AccountForm()
                    form.errors['check_pass'] = ["Please re-enter this as well to update password."]

                elif len(password) < 8                                                          \
                or not any(char.isdigit() for char in password)                                 \
                or not any(char.isupper() for char in password)                                 \
                or not any(char.islower() for char in password)                                 \
                or not any(not char.isalnum() for char in password)                             \
                or not any(char in ALLOWED_SPECIAL_CHAR for char in password):
                    print("In here")
                    form = AccountForm()
                    form.errors['password'] = ["Password does not match criteria."]

                elif check:
                    if password != check:
                        form = AccountForm()
                        form.errors['check_pass'] = ["Passwords must match."]

                    else:
                        user.set_password(password)
                        user.save(update_fields=['password'])
                        messages.success(request, "Password updated successfully. Please re-login with new password.")
                        return redirect('login')

            if pic:
                user = UserImage.objects.get(user=request.user)
                user.image = pic
                user.save(update_fields=['image'])

                size = (200, 200)
                pic = Image.open(user.image)
                pic.thumbnail(size)
                pic.save(user.image.path)

                return redirect('useraccount')

    else:
        form = AccountForm()

    frontend = {'form': form}
    return render(request, 'blog/account.html', frontend)


@login_required
def createblog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Your new blog is created successfully. It is yet to be published.")
            return redirect('home')

    else:
        form = BlogForm()

    frontend = {'form': form}
    return render(request, 'blog/create.html', frontend)


@login_required
def postblog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.posted_on = timezone.now()
            post.save()

            messages.success(request, "Your new blog is posted successfully.")
        
        else:
            return redirect('createblog', {'form': form})

    return redirect('home')


@login_required
def publishblog(request):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, pk=request.POST.get('blogid'))
        post.posted_on = timezone.now()
        post.save()

        messages.success(request, "Your blog is posted successfully.")

    blogs = BlogPost.objects.filter(posted_on=None, author=request.user)
    paginator = Paginator(blogs, 2)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    if not page_num or int(page_num) <= paginator.num_pages:
        frontend = {'blogs': blogs, 'page': page}
        return render(request, 'blog/publish.html', frontend)
    
    else:
        return render(request, 'error/404.html')


@login_required
def editblog(request, blogid, returnpage):
    post = get_object_or_404(BlogPost, pk=blogid)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            messages.success(request, "Blog edited successfully.")

        if returnpage == "publishblog":
            return redirect(returnpage)

        else:
            return redirect(returnpage, blogid)

    else:
        form = BlogForm(instance=post)

        frontend = {'form': form, 'returnpage': returnpage, 'blogid': blogid}
        return render(request, 'blog/edit.html', frontend)


@login_required
def deleteblog(request, blogid):
    post = get_object_or_404(BlogPost, pk=blogid)
    post.delete()

    messages.success(request, "Blog deleted sucessfully.")
    return redirect('home')


def authorpage(request, author):
    author = get_object_or_404(User, username=author)
    posts = BlogPost.objects.filter(author=author, posted_on__lte=timezone.now()).order_by('-posted_on')

    frontend = {'author': author, 'posts': posts}
    return render(request, 'blog/authorpage.html', frontend)


def blogpage(request, blogid):
    blog = get_object_or_404(BlogPost, pk=blogid)
    form = CommentForm()

    frontend = {'blog': blog, 'form': form}
    return render(request, 'blog/blog.html', frontend)


@login_required
def createcomm(request, blogid):
    post = get_object_or_404(BlogPost, pk=blogid)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            messages.success(request, "Comment sent for approval. Once approved, it will appear in comments section below.")

        return redirect('blogpage', blogid)


@login_required
def editcomm(request, comid):
    if request.method == 'POST':
        comment = get_object_or_404(Comments, pk=comid)
        comment.comment = request.POST.get('edt-comment')
        comment.save()

        messages.success(request, "Comment edited successfully.")
        return redirect('blogpage', comment.post.id)


@login_required
def deletecomm(request, comid):
    if request.method == 'POST':
        comment = get_object_or_404(Comments, pk=comid)
        comment.delete()

        messages.success(request, "Comment deleted successfully.")
        return redirect('blogpage', comment.post.id)


@login_required
def approvallist(request):
    allblogs = BlogPost.objects.filter(posted_on__lte=timezone.now())
    blogs = []
    for blog in allblogs:
        if blog.unapproved_comments():
            blogs.append(blog)

    paginator = Paginator(blogs, 2)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    if not page_num or int(page_num) <= paginator.num_pages:
        frontend = {'blogs': blogs, 'page': page}
        return render(request, 'blog/approvallist.html', frontend)
    
    else:
        return render(request, 'error/404.html')


@login_required
def approvecomm(request, comid):
    comment = get_object_or_404(Comments, pk=comid)
    comment.approve()

    if comment.post.unapproved_comments():
        return redirect('blogpage', comment.post.id)
    else:
        return redirect('approvallist')


@login_required
def deleteaccount(request, userid):
    user = get_object_or_404(User, pk=userid)
    user.delete()
    
    messages.success(request, "Account deleted successfully.")
    return redirect('logout')