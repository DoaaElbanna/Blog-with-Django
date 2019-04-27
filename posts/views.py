from urllib.parse import quote
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect,  Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post
from django.urls import reverse


# Function based views


def post_create(request):
    # assume the user is authenticated
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404("Oh, Sorry you must be logged in")

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user  # assume that the user logged in
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, pk):  # retrieve
    instance = get_object_or_404(Post, id=pk)
    share_string = quote(instance.content)
    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None  # To be sure is exist
        # To be sure the parent id is exist
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            # run a query set filter to see if the parent ID is in database
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
        if created:
            print("Yah it worked")
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form
    }
    return render(request, 'post_detail.html', context)


def post_list(request):  # list items
    queryset_list = Post.objects.all()
    query = request.GET.get("query")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    contacts = paginator.get_page(page)
    return render(request, 'list.html', {'contacts': contacts})
    context = {
        "title": "List",
        "contacts": contacts,
        "page_request_var": page_request_var,
    }
    return render(request, 'list.html', context)


def post_update(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404("that's not allowed")
    instance = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # messages.success(request, "Great, is saved !")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {"title": instance.title, "instance": instance, "form": form}
    return render(request, 'post_form.html', context)


def post_delete(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404("that's not allowed")
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    # messages.success(request, "It was deleted !")
    return redirect("posts:list")



