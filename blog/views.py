from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.db.models import Count, Q
from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()


@staff_member_required
def un_comments(request):
    unapproved_comments = Comment.objects.filter(is_approved=False)
    return render(request, 'blog/unapproved_comments.html', {
        'comments': unapproved_comments
    })


@staff_member_required
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    return redirect('blog:unapproved_comments')


@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('blog:unapproved_comments')


class PostListView(View):
    def get(self, request):
        posts = Post.objects.annotate(
            approved_comment_count=Count('comments',
                                         filter=Q(comments__is_approved=True))
                                      ).order_by('-created_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


class CreatePostView(LoginRequiredMixin, UserPassesTestMixin, View):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        form = self.PostForm()
        return render(request, 'blog/post_form.html', {'form': form})

    def post(self, request):
        form = self.PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:post_list')
        return render(request, 'blog:post_form.html', {'form': form})

    class PostForm(forms.ModelForm):
        has_code_block = forms.BooleanField(required=False, label="Содержит компьютерный код")

        title = forms.CharField(
            label='Title',
            widget=forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'required': True,
            })
        )
        content = forms.CharField(
            label='Content',
            widget=forms.Textarea(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'rows': '4',
                'required': True,
            })
        )
        author = forms.ModelChoiceField(
            label='Author',
            queryset=User.objects.all(),
            widget=forms.Select(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'required': True,
            })
        )
        created_date = forms.DateTimeField(
            label='Created Date',
            input_formats=['%Y-%m-%d %H:%M:%S'],
            widget=forms.DateTimeInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'type': 'datetime-local',
                'required': True,
            })
        )
        image = forms.ImageField(
            label='Image',
            required=False,
            widget=forms.FileInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
            })
        )

        class Meta:
            model = Post
            fields = ['title', 'content', 'author', 'created_date', 'image', 'has_code_block']


class PostDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        approve_comments = post.comments.filter(is_approved=True)
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'comment_form': self.CommentForm(),
            'comments': approve_comments,
        })

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = self.CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('blog:post_detail', pk=post.pk)
        comments = post.comments.filter(is_approved=True)
        return render(request, 'blog/post_detail.html', {
            'post': post,
            'comment_form': comment_form,
            'comments': comments,
        })

    class CommentForm(forms.ModelForm):
        content = forms.CharField(
            label='Comment',
            widget=forms.Textarea(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'rows': '4',
                'required': True,
            })
        )
        author = forms.ModelChoiceField(
            label='Author',
            queryset=User.objects.all(),
            widget=forms.Select(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'required': True,
            })
        )

        class Meta:
            model = Comment
            fields = ['author', 'content']


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Post
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get(self, request, pk):
        post = self.get_object()
        form = self.PostForm(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        post = self.get_object()
        form = self.PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user

    class PostForm(forms.ModelForm):
        title = forms.CharField(
            label='Title',
            widget=forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'required': True,
            })
        )
        content = forms.CharField(
            label='Content',
            widget=forms.Textarea(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
                'rows': '4',
                'required': True,
            })
        )
        image = forms.ImageField(
            label='Image',
            required=False,
            widget=forms.FileInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                         ' focus:outline-none focus:ring focus:ring-blue-500',
            })
        )

        class Meta:
            model = Post
            fields = ['title', 'content', 'image']


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def get(self, request, pk):
        post = self.get_object()
        return render(request, self.template_name, {'object': post})

    def post(self, request, pk):
        post = self.get_object()
        post.delete()
        return redirect(self.success_url)

    def test_func(self):
        post = self.get_object()
        return self.request.user.is_staff or post.author == self.request.user


def get_post_comments(request, post_id):
    try:
        comments = Comment.objects.filter(post_id=post_id).values('author', 'content')
        return JsonResponse(list(comments), safe=False)
    except Exception as e:
        print(f'Error fetching comments: {e}')
        return JsonResponse({'error': 'Error fetching comments'}, status=500)
