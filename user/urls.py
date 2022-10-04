from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>/', views.user_follow, name='user-follow'),
    path('user/profile/<int:id>/', views.user_profile_view, name='user-profile'),
    path('user/fix_profile/', views.profile_edit, name='profile'), # 프로필 수정
    
]
