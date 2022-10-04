import email
from django.shortcuts import render, redirect
from .models import UserModel
from tweet.models import TweetModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model  # 사용자가 있는지 검사하는 함수
from django.contrib import auth  # 사용자 auth 기능
from django.contrib.auth.decorators import login_required
import re  # 정규표현식 모듈



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

            exist_email = get_user_model().objects.filter(email=email)
            # 이메일 유효성 검사
            if email != '':
                email_regex = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')  # 정규표현식 컴파일
                email_validation = email_regex.match(email)

                if email_validation == None:
                    return render(request, 'user/signup.html',
                                  {'error': '이메일 형식이 아닙니다.'})
                elif exist_email:
                    return render(request, 'user/signup.html',
                                  {'error': '이미 존재하는 이메일입니다.'})

                UserModel.objects.create_user(username=username, password=password, email=email,
                                              author_name=author_name)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        email = request.POST.get('email',"")
        author_name = request.POST.get('author_name',"")

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


# 프로필수정페이지 만들기
# def fix_profile(request):
    
#     if request.method == 'POST':
#         form = fix_profile(request.POST, request.FILES, instance=request.user)


@login_required
def profile_edit(request):
    if request.method == "POST":
        """
        현재 유저의 프로필을 가져오고
        받은 값으로 프로필을 갱신한다.
        """
        user = request.user
        old_profile = UserModel.objects.get(username=user)
        old_profile.author_name = request.POST.get('author_name','')
        old_profile.email = request.POST.get('email','')
        old_profile.bio = request.POST.get('bio','')
        old_profile.save()
        return redirect('/tweet')   # 프로필 페이지 넣기
    elif request.method == "GET":
        return render(request, 'user/fix_profile.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        # 사용자 중 내가 팔로우 한 사람들만 나오게하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        
        follow = UserModel.objects.filter(followee = request.user)

        return render(request, 'user/user_list.html', {'user_list': follow})


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
def user_profile_view(request,id): # 사용자 프로필 조회
    if request.method == 'GET':

        user = UserModel.objects.get(id=id)
        my_tweet_count = TweetModel.objects.filter(author=id).count() # 본인 게시글 갯수 집계
        my_tweet = TweetModel.objects.filter(author=id) # 본인 게시글 가져오기
        view_user = UserModel.objects.get(username=request.user.username)
        
        return render(request, 'user/user_profile.html', {'user' : user, 'my_tweet_count':my_tweet_count, 'view_user':view_user, 'my_tweet':my_tweet})


@login_required 
def user_follow(request, id): # 사용자 프로필 페이지에서 팔로잉/팔로우
    
    me = request.user
    click_user = UserModel.objects.get(id=id)
    
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect(f'/user/profile/{click_user.id}')

@login_required
def followee_view(request, id):
    me = request.user
    user = UserModel.objects.get(id=id) #user id값을 받아서 user class 정보로 찾겠다는 거(기준은 id)     
    user_list = UserModel.objects.all().exclude(username=request.user.username)
    follow = UserModel.objects.filter(follow = user) 

    return render(request,'user/followee_list.html',{"user_list":follow})

@login_required
def follow_view(request, id):
    me = request.user
    user = UserModel.objects.get(id=id) #user id값을 받아서 user class 정보로 찾겠다는 거(기준은 id)     
    user_list = UserModel.objects.all().exclude(username=request.user.username)
    followee = UserModel.objects.filter(followee = user) 

    return render(request,'user/follow_list.html',{"user_list":followee})

# 프로필 수정시 기존 내용 보여주기
@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})
