from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from ast import literal_eval
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.models import Profile,Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
#from account.models import Accept
from .forms import CreateBlogPostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# we use class based view for  create delete or update post
# diff kind of list view ,details view update and delete view,create view
# list view

# by default django check html file in templates directorys so we create templates directory in this we create blog directory for accessing index.html we need to write blog/index.html for check in blog directory and take index.html
def home(request):
    Cuser = request.user;
    try:
        Friends = []
        if str(Cuser.profile.friends) != "-":
            Fri = literal_eval(Cuser.profile.friends)
            print(type(Fri))
            for item in Fri.items():
                Friends.append(item)
        else:
            Fri = {}
        context = {
            'posts': Post.objects.all(),
            'Friends':Friends
        }
        paginate_by = 4
        return render(request, 'blog/home.html', context)
    except:
        context = {
            'posts': Post.objects.all(),
            'Friends':'null'
        }
        return render(request, 'blog/home.html', context)
# it same as home function view we use class view
def profile(request):
    user=request.GET;
    # print(user)
    profile=Profile.objects.filter(id=user)
    #u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=user.profile)
    context = {
        'p_form':p_form,
    }

    return render(request, 'blog/profile.html', context)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-pub_date')

class PostListView(ListView):
    context = {
        'posts': Post.objects.all(),
    }
    model=Post
    template_name = 'blog/home.html'
    context_object_name = 'posts' # it used to pass all posts as key and value pair of dictionary so we can use in home.html page
    ordering = ['-pub_date']
    paginate_by = 4
    # def get_queryset(self):
    #     user=self.request.user;
    #     Friends = []
    #     try:
    #         if str(user.profile.friends) != "-":
    #             Fri = literal_eval(user.profile.friends)
    #             print(type(Fri))
    #             for item in Fri.items():
    #                 Friends.append(item)
    #         else:
    #             Fri = {}
    #     except:
    #
    #     return {'posts': Post.objects.all(), 'Friends': Friends}



    # it is columns name which you want to order base on that column
    # for - to go from newest date to oldest date
# class base view bydefault check for default template_page it is blog/post_list.html
#<app>/<model>_<viewtype>.html
class PostDetailView(DetailView):
    model=Post

# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title','head0','chead0','head1','chead1','head2','chead2','thumbnail','video','content']
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return redirect('blog-home')
# #
# #
# #
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['title', 'head0', 'chead0', 'head1', 'chead1', 'head2', 'chead2', 'thumbnail', 'video', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def create_blog_view(request):
    context = {}
    user = request.user
    print(user)
    print(user.username)
    if not user.is_authenticated:
        return redirect('blog-home')
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author=User.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, "blog/create_blog.html", context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    #form = ImageUploadForm(request.POST, request.FILES)
    thumbnail=forms.FileField()
    fields = ['title', 'head0', 'chead0', 'head1', 'chead1', 'head2', 'chead2', 'thumbnail', 'video', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ['title', 'head0', 'chead0', 'head1', 'chead1', 'head2', 'chead2', 'thumbnail', 'video', 'content']
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.save()
#         return
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False

# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = ExampleModel.objects.get(pk=course_id)
#             m.model_pic = form.cleaned_data['image']
#             m.save()
#             return HttpResponse('image upload success')
#     return HttpResponseForbidden('allowed only via POST')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def blogPost(request, id):
    post = Post.objects.filter(id =int(id))[0]
    #print(post)
    max1=Post.objects.all();
    first1=Post.objects.first();
    last1=Post.objects.last();
    return render(request, 'blog/blogPost.html',{'post':post,'prev':int(id-1),'next':int(id+1),'first':first1,'last':last1,'title': 'blogPost'})

@login_required
def search(request):
    query=request.POST.get('search')
    users =User.objects.all()
    print(users)
    posts=Post.objects.all()
    #return HttpResponseRedirect('/', {'username': request.user.username, 'uw': uw})
    allPosts = []
    if len(query)==0:
        return redirect('blog-home')
    if len(query)!=0:
        for user in users:
            if query==user.username.lower():
                search_list=Post.objects.filter(author=user)
                allPosts=search_list
        if len(allPosts)==0:
            for post in posts:
                if query in post.title:
                    allPosts.append(post);
    #search_list = Searches.objects.filter(user_id=user.id)
    params={'allPosts':allPosts,'msg':""}
    if len(allPosts) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'blog/search.html', params)


class FollowsListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'blog/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data

