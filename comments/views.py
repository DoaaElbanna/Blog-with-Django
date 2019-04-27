from django.contrib import messages
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import Comment
from .forms import CommentForm
from django.urls import reverse


# Create your views here.

@login_required
def comment_delete(request, pk):
    # obj = get_object_or_404(Comment, id=pk)
    try:
        obj = Comment.objects.get(id=pk)
    except:
        raise Http404

    if obj.user != request.user:  # Check the user has a permission to delete
        # messages.success(request, "You don't have a permission to view this")
        # raise Http404
        response = HttpResponse("You don't have a permission to view this")
        response.status_code = 403  # 403 stands for you don't have a permission
        return response
    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        # messages.success(request, "This has been deleted")
        return HttpResponseRedirect(parent_obj_url)
    context = {
        "object": obj
    }
    return render(request, "confirm_delete.html", context)


def comment_thread(request, pk):
    # obj = get_object_or_404(Comment, id=pk)
    try:
        obj = Comment.objects.get(id=pk)
    except:
        raise Http404

    if not obj.is_parent:
        obj = obj.parent
    content_object = obj.content_object
    content_id = obj.content_object.id
    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id,
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
    context = {
        "comment": obj,
        "form": form
    }
    return render(request, "comment_thread.html", context)
