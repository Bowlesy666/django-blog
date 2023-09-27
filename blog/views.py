from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # set the email and name auto' from user thats logged in
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            # save comment but not commit to db yet
            comment = comment_form.save(commit=False)
            # first we assign a post to it
            comment.post = post
            # then we can save it
            comment.save()
        else:
            # if form not valid we return empty comment instance
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug):
        # first, get the post we intend to toggle the like on
        post = get_object_or_404(Post, slug=slug)

        # if the post has a like from this user id already
        if post.likes.filter(id=request.user.id).exists():
            # remove like
            post.likes.remove(request.user)
        else:
            # add a like
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
