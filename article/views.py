from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import ArticlePost
import markdown
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.


def article_list(request):
    articles_list = ArticlePost.objects.all()
    #设置每页显示1篇文章
    paginator = Paginator(articles_list,9)
    #获取url中的页码
    page = request.GET.get('page')
    #返回对应页码的文章给articles
    articles = paginator.get_page(page)
    context = {'articles':articles}
    return render(request,'article/list.html',context)


def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)

    #update_fields=[]指定了数据库只更新total_views字段，优化执行效率
    article.total_view += 1
    article.save(update_fields=['total_view'])

    article.body = markdown.markdown(article.body,
    extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    context = {'article':article}
    return render(request,'article/detail.html',context)


def article_created(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单内容有误，请重新输入。')
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request,'article/created.html',context)


def article_safe_delete(request, id):
    if request.method == "POST":
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse("仅仅允许post请求。")


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)

    if request.user != article.author:
        return HttpResponse("您没有权限修改次文章。")

    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail',id=id)
        else:
            return HttpResponse('表单内容有误，请重新输入。')
    else:
        article_post_form = ArticlePostForm()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request,'article/update.html',context)
