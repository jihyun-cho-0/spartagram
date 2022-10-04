import email
from django.shortcuts import render, redirect
from .models import UserModel
from tweet.models import TweetModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 있는지 검사하는 함수
from django.contrib import auth  # 사용자 auth 기능
from django.contrib.auth.decorators import login_required
import re # 정규표현식 모듈


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        author_name = request.POST.get('author_name', '')


        if password != password2:
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 패스워드는 필수값 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html',
                              {'error': '사용자가 이미 존재합니다.'})  # 중복이름 있으니 로그인페이지 다시 띄움, 경고메세지도 넣음 좋을듯
            
            # 이메일 유효성 검사
            if email != '':
                email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$') # 정규표현식 컴파일
                email_validation = email_regex.match(email)
                
                if email_validation == None:
                    return render(request, 'user/signup.html',
                                {'error': '이메일 형식이 아닙니다.'}) 

                UserModel.objects.create_user(username=username, password=password, email=email, author_name=author_name)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        me = auth.authenticate(request, username=username, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': '유저이름 혹은 패스워드를 확인해주세요.'})  # 로그인 실패
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')


@login_required
def user_profile_view(request,id): # 사용자 프로필
    if request.method == 'GET':

        user = UserModel.objects.get(id=id)
        my_tweet_count = TweetModel.objects.filter(author=id).count() # 게시글 갯수 집계
        # view_user = request.user # 해당 프로필 페이지를 요청한 사용자
        view_user = UserModel.objects.get(username=request.user.username)
        return render(request, 'user/user_profile.html', {'user' : user, 'my_tweet_count':my_tweet_count, 'view_user':view_user})


@login_required 
def user_follow(request, id): # 사용자 프로필 페이지에서 팔로잉/팔로우 (작업중)
    me = request.user
    click_user = UserModel.objects.get(id=id)

    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('user/profile/<int:id>')