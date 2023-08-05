from django.shortcuts import render , get_object_or_404 , redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
def welcome(request):
    return render(request , 'blog/post/welcome.html')


def index(request):
    return render(request , 'blog/post/index.html')


def postlist(request):
    posts = Post.objects.all()
    return render(request , 'blog/post/list.html' , {"posts" : posts})


def postdetail(request , slug):
    post = get_object_or_404(Post, slug = slug)
    comments = post.comments.filter(active = True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():

            new_comment = comment_form.save(commit = False)       # Create Comment object but don't save to database yet
            new_comment.post = post     # Assign the current post to the comment
            new_comment.save()      # Save the comment to the database
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request , 'blog/post/detail.html' , context)



def UserAccount(request):
    user = request.user
    try:
        account = Account.objects.get(user = user)
    except:
        account = Account.objects.create(user = user)
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['last_name']
            account.gender = form.cleaned_data['gender']
            account.address = form.cleaned_data['address']
            account.age = form.cleaned_data['age']
            account.phone = form.cleaned_data['phone']
            user.save()
            account.save()
            return redirect('blog:index') #if form was valid go to blog/index
        else:
            return render(request , 'blog/forms/account_form.html' , {'form' : form , 'account' : account})
    form = AccountForm()
    return render(request , 'blog/forms/account_form.html' , {'form' : form , 'account' : account})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'] , cd['email'] , cd['password'])
            messages.success(request , 'ثبت نام موفقیت آمیز بود', 'success') #show this message if registration form is successful
            return redirect('blog:index')#if form was valid go to blog/index
    else:
        form = UserRegistrationForm()
    return render(request , 'blog/forms/register_form.html' , {'form' : form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username = cd['username'] , password = cd['password']) #check if user/pass is correct
            if user is not None:
                login(request , user)
                messages.success(request , 'ورود موفقیت آمیز بود', 'success') #show this message if login form is successful
                return redirect('blog:index') #if form was valid go to blog/index
            else:
                messages.error(request , 'نام کاربری یا رمز عبور اشتباه است' , 'danger')
    else:
        form = UserLoginForm()
    return render(request , 'blog/forms/login_form.html' , {'form' : form})


def user_logout(request):
    logout(request)
    messages.success(request , 'خروج موفقیت آمیز' , 'success') #show this message if logout form is successful
    return redirect('blog:index')


def search(request):
    if request.method == 'POST':
        query_name = request.POST.get('search_input')
        if query_name:

            results = Post.objects.filter(status = 'published', body__contains = query_name)
            return render(request , 'blog/post/search_field.html', {'results': results , 'query': query_name})

        else:
            return render(request , 'blog/post/search_field.html', {'results': None , 'query': query_name})

    return render(request , 'blog/post/search_field.html' , {'results': None , 'query' : None})

def user_profile(request):
    pass