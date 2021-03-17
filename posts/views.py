from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


@login_required(login_url='login/')
def post_comment_create_list_view(request):
    posts_form = PostForm()
    comment_form = commentForm()
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    if 'submit_comment_form' in request.POST:
        comment_form = commentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = profile
            comment.post = Post.objects.get(id=request.POST.get('post_id'))
            comment.save()
            comment_form = commentForm()
    if 'submit_posts_form' in request.POST:
        posts_form = PostForm(request.POST, request.FILES)
        if posts_form.is_valid():
            instance = posts_form.save(commit=False)
            instance.author = profile
            instance.save()
            posts_form = PostForm()
    context = {
        'qs': qs,
        'profile': profile,
        'posts_form': posts_form,
        'comment_form': comment_form,
    }
    return render(request, 'posts/main.html', context)


def like_unlike(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        the_post = Post.objects.get(id=post_id)
        if profile in the_post.liked.all():
            the_post.liked.remove(profile)
        else:
            the_post.liked.add(profile)
        like, created = Likes.objects.get_or_create(user=profile, post_id=post_id)
        if not created:
            if like.value == 'like':
                like.value = 'unlike'
            else:
                like.value = 'like'
        else:
            like.value = 'like'

        like.save()
        the_post.save()
        return redirect('/')


class post_delete_view(DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:main_post_view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'you need to be the author of the post to delete it')
        return obj


class post_update_view(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main_post_view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, "you need to be the autor of the post to update it")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super()
