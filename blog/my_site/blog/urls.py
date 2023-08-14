from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('' , views.index , name = 'index'),
    path('postlist/' , views.postlist , name = 'post_list'),
    path('postlist/create/', views.create_post, name='create_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('postdetail/<slug:slug>/' , views.postdetail , name = 'post_detail'),
    path('account-form/' , views.UserAccount , name = 'account_form'),
    path('register-form/', views.user_register, name='user_register'),
    path('login/' , views.user_login , name = 'user_login'),
    path('logout/' , views.user_logout , name = 'logout'),
    path('search/' , views.search , name='search'),

]
