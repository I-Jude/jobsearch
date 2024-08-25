from django.urls import path
from . import views

urlpatterns =[
    path('login/', views.login_1,name='login_1'),
    path('register/', views.register, name='register'),
    path('user_profile_edit/', views.user_profile_edit, name='user_profile_edit'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage_opportunities/',views.manage_opportunities, name='manage_opportunities'),
    path('edit_opportunity/<int:pk>/',views.edit_opportunity, name='edit_opportunity'),
    path('delete_opportunity/<int:pk>/',views.delete_opportunity,name='delete_opportunity'),
    path('logout/', views.logout_view, name='logout'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('apply_opportunity/', views.apply_opportunity, name='apply_opportunity'),
    path('my-applications/', views.user_applications, name='user_applications'),
]