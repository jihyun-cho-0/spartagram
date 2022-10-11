# tweet/urls.py
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'), # 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결
    path('tweet/', views.tweet, name='tweet'), # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
    path('tweet/modify/<int:id>', views.modify_tweet, name='modify-tweet'),
    path('tweet/<int:id>',views.detail_tweet,name='detail-tweet'),
    
    path('tweet/home/commentadd/<int:id>', views.main_write_comment, name='add-comment'),
    path('tweet/follow/<int:id>/', views.user_follow, name='user-follow'),

    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tweet/comment/correction/<int:id>', views.correction_comment, name='correction-comment'),
    path('tweet/comment/follow/<int:id>', views.comment_like, name='comment-like'),
    path('tweet/like/<int:id>', views.feed_like, name='feed-like'),
    path('tweet/save/<int:id>', views.feed_save, name='feed-save'),

    path('tweet/create/', views.tweet_write, name='create'), # user가 바뀌더라도 게시물 작성 페이지 나오게하기
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),

]