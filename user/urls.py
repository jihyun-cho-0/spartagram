from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>/', views.user_follow, name='user-follow'),
    path('user/profile/<int:id>/', views.user_profile_view, name='user-profile'),
    path('user/profile/follow/<int:id>/', views.follow_view, name='follow-list'), #팔로우(팔로잉) 모달창 
    path('user/profile/followee/<int:id>/', views.followee_view, name='follewee-list'), #팔로이(팔로워) 모달창
    path('user/fix_profile/', views.profile_edit, name='profile'), # 프로필 수정
 ] 
