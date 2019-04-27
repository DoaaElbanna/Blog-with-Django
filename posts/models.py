from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
from comments.models import Comment
from .utils import get_time_read

# MVC Model View Controller
# class PostQuerySet(models.query.QuerySet):
#     def not_draft(self):
#         return self.filter(draft=False)
#
#     def published(self):
#         return self.filter(publish__lte=timezone.now()).not_draft()
#
#
# class PostManger(models.manager):
#     def get_queryset(self, *args, **kwargs):
#         return PostQuerySet(self.model, using=self._db)
#
#     def active(self, *args, **kwargs):
#         # Post.objects.all() = super(PostManager, self).all()
#         return self.get_queryset().published()


def upload_location(instance, filename):
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    return "%s/%s" % (new_id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
            width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)  # models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # objects = PostManger()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.id})  # url name, args of view
        # return "posts/%s/" % self.id

    def get_api_url(self):
        return reverse("posts-api:detail", kwargs={"pk": self.id})  # url name, args of view

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        contenttype = ContentType.objects.get_for_model(instance.__class__)
        return contenttype

    class Meta:
        ordering = ["-timestamp", "-updated"]  # order posts


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    query_set = Post.objects.filter(slug=slug).order_by("-id")
    exists = query_set.exists()
    if exists:
        new_slug = "%s-%s" % (slug, query_set.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_time_read(html_string)
        instance.read_time = read_time_var  # set the value to read_time field


pre_save.connect(pre_save_post_receiver, sender="posts.Post")










