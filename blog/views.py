from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone

from .models import BlogPost

# Create your views here.
def home(request):
    blogs = BlogPost.objects.filter(posted_on__lte=timezone.now()).order_by('-posted_on')
    paginator = Paginator(blogs, 2)

    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)

    frontend = {'blogs': blogs, 'page': page}
    return render(request, 'blog/home.html', frontend)


def about(request):
    return render(request, 'blog/about.html')