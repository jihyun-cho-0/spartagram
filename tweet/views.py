from itertools import count
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment
from user.models import UserModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.db.models import Count
import os

# Create your views here.
def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


# tweet/views.py

@login_required
def tweet(request):
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        #aonnotate : 오브젝트에 원하는 값 추가
        all_tweet = TweetModel.objects.all().annotate(comment_count=Count('tweetcomment')).order_by('-created_at')
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'tweet/home.html', {'tweet': all_tweet, 'user_list':user_list})

    elif request.method == 'POST':  # 요청 방식이 POST 일때
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        title = request.POST.get('my-title','')
        content = request.POST.get('my-content', '')  # 글 작성이 되지 않았다면 빈칸으로
        img = request.FILES.get("imgfile")
        tags = request.POST.get('tag', '').split('#')
        if content == '' or title == '':  # 글이 빈칸이면 기존 tweet과 에러를 같이 출력
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '제목이나 글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content, title=title, imgfile=img)  # 글 저장을 한번에!
            for tag in tags:
                tag = tag.strip()
                if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    
    if my_tweet.imgfile!='':
        path = '.'+my_tweet.imgfile.url
        if os.path.isfile(path):
            os.remove(path)
    my_tweet.delete()
    return redirect('/tweet')

def modify_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        return render(request, 'tweet/tweet_modify.html', {'tweet': my_tweet})

    elif request.method == 'POST':
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        title = request.POST.get('my-title','')
        content = request.POST.get('my-content', '')  # 글 작성이 되지 않았다면 빈칸으로
        tags = request.POST.get('tag', '').split('#')
        if content == '' or title == '':  # 글이 빈칸이면 기존 tweet과 에러를 같이 출력
            return render(request, 'tweet/tweet_modify.html', {'error': '제목이나 글은 공백일 수 없습니다'})
        else:
            my_tweet.user = user
            my_tweet.title = title
            my_tweet.content = content
            my_tweet.tags.clear()
            for tag in tags:
                if tag != '':
                    tag = tag.strip()
                    if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                        my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet/' + str(id))

@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    like_list = TweetModel.objects.all().exclude(title=my_tweet.title)
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment,'like_list':like_list})

@login_required
def main_write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        return redirect('/tweet')




@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()
        return redirect('/tweet/' + str(id))

@login_required
def correction_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("correction_comment", "")
        before_comment = TweetComment.objects.get(id=id)
        tweet_id = before_comment.tweet_id
        before_comment.comment = comment
        before_comment.save()
        return redirect('/tweet/' + str(tweet_id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(current_tweet))


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

@login_required
def comment_like(request, id):
    me = request.user
    click_user = TweetModel.objects.get(id=id)
 
    if me in click_user.like_content.all():
        click_user.like_content.remove(request.user)
    else:
        click_user.like_content.add(request.user)
    return redirect('/tweet/'+str(id))


@login_required
def feed_like(request, id):
    me = request.user
    click_user = TweetModel.objects.get(id=id)
 
    if me in click_user.like_content.all():
        click_user.like_content.remove(request.user)
    else:
        click_user.like_content.add(request.user)
    return redirect('/tweet')

@login_required
def feed_save(request, id):
    me = request.user
    click_user = TweetModel.objects.get(id=id)
 
    if me in click_user.save_content.all():
        click_user.save_content.remove(request.user)
    else:
        click_user.save_content.add(request.user)
    return redirect('/tweet')


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/tweet')

@login_required
def tweet_write(request):
    if request.method == 'GET':
        return render(request, 'tweet/tweet_create.html')

