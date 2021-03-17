from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse


# from posts.models import *

class ProfileManager(models.Manager):
    def get_all_profiles_to_invites(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(reciever=profile))
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.reciever)
                accepted.add(rel.sender)
        avilable = [profile for profile in profiles if profile not in accepted]
        return avilable

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, default="no bio.......")
    email = models.EmailField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(default='avatar.jpg', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'slug': self.slug})


    def get_friends(self):
        return self.friends.all()


    def get_friends_no(self):
        return self.friends.all().count()


    def get_likes_no(self):
        return self.post_likes.all().count()


    def get_posts_no(self):
        return self.Post_set.all().count()


    def get_all_authors_posts(self):
        return self.Post_set.all()

    # def get_likes_given_no(self):
    #     likes = self.likee.all()
    #     total_liked = 0
    #     for item in likes:
    #         if item.value == 'like':
    #             total_liked += 1
    #     return total_liked


    def get_likes_given_no(self):
        total_liked = self.likee.filter(value='like').count()
        return total_liked


    def get_liked_recieved_no(self):
        posts = self.Post_set.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked


__initial_first_name = None
__initial_last_name = None


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__initial_first_name = self.first_name
    self.__initial_last_name = self.last_name


def save(self, *args, **kwargs):
    ex = False
    to_slug = self.slug
    if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or not self.slug:
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
    self.slug = to_slug
    super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitation_recieved(self, reciever):
        qs = Relationship.objects.filter(reciever=reciever, status='send')
        return qs


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reciever')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.reciever}-{self.status}"
