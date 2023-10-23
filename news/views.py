from .models import Post
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Post


def news_list(request):
    news = Post.objects.all()
    return render(request, 'news_list.html', {'news': news})


def news_detail(request, pk):
    news = get_object_or_404(Post, pk=pk)
    return render(request, 'news_detail.html', {'news': news})
