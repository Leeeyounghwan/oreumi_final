from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import TogetherPost,TogetherComment

# from .forms import CommentForm

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, User, Report,Schedule,ScheduleComment
from django.contrib.auth.decorators import login_required
import openai
from django.http import JsonResponse
import json
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .forms import UserProfileForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

#마이페이지 by 준경

#@login_required
def profile(request): #내 정보 수정
    user = request.user
    form = UserProfileForm(initial={'username': user.username})

    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            if username != user.username:
                user.username = username
                user.save()
                messages.success(request, '아이디가 업데이트되었습니다.')

            if password:
                if password == password_confirm:
                    user.set_password(password)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '비밀번호가 업데이트되었습니다.')
                else:
                    messages.error(request, '비밀번호와 비밀번호 확인이 일치하지 않습니다.')

            return redirect('profile')

    return render(request, 'mypage/profile.html', {'form': form})

def mytopics(request):#내가 쓴 글 보기
  return render(request, 'mypage/mytopics.html', {'posts' : TogetherPost.objects.all()})

def myreviews(request): #내가받은 후기 보기
    return render(request,'mypage/myreviews.html')

def like_schedule(request): #찜한 일정 리스트
    return render(request,'mypage/like_schedule.html',{'schedules' : Schedule.objects.all()})

def chatting_room(request): #채팅방리스트
    return render(request,'mypage/chatting_room.html')



# 관리자페이지 시작 by 영환
def main(request):
    return render(request, "main.html")

def admin_check(request):
    if request.user.is_authenticated:
        user = request.user.username
        user_info = get_object_or_404(User, username=user)
        if user_info.is_staff == True :
            return True
        else:
            return False

def admin_page(request):

    # if admin_check(request) == True :
    #     return redirect("trip:admin_page")
    # else:
        return render(request, "admin/admin_page.html")


def create_product(request):

    # if admin_check(request) == True :
    return render(request, "admin/create_product.html")
    # else:
    #     return redirect("trip:main")

def product_management(request):

    packages = Package.objects.all()
    context = {
        "packages" : packages
    }
    return render(request, "admin/product_management.html", context)

    # if admin_check(request) == True :
    #     packages = Package.objects.all()
    #     context = {
    #         "packages" : packages
    #     }

    #     return render(request, "admin/product_management.html", context)
    # else:
    #     return redirect("trip:main")    

def deleted_product(request):

    deleted_packages = Package.objects.filter(is_deleted=True).order_by('-updated_at')
    context = {
        "deleted_packages" : deleted_packages
    }
    return render(request, "admin/deleted_product.html", context)

    # if admin_check(request) == True :
    #     deleted_packages = Package.objects.filter(is_deleted=True).order_by('-updated_at')
    #     context = {
    #         "deleted_packages" : deleted_packages
    #     }

    #     return render(request, "admin/deleted_product.html", context)
    # else:
    #     return redirect("trip:main")

def order_inquiry(request):
    return render(request, "admin/order_inquiry.html")

def delivery_tracking(request):
    return render(request, "admin/delivery_tracking.html")

def return_management(request):
    return render(request, "admin/return_management.html")

def report_detail(request):

    if admin_check(request) == True :
        reports = Report.objects.all()
        context = {
            "reports" : reports
        }

        return render(request, "admin/report_detail.html", context)
    else:
        return redirect("trip:main")

def user_management(request):

    if admin_check(request) == True :
        users = User.objects.all()
        context = {
            "users" : users
        }

        return render(request, "admin/user_management.html", context)
    else:
        return redirect("trip:main")

def blacklist_management(request):

    if admin_check(request) == True :
        blacklist = User.objects.filter(is_black=True)
        context = {
            "blacklist" : blacklist
        }

        return render(request, "admin/blacklist_management.html", context)
    else:
        return redirect("trip:main")


# 관리자페이지 종료


#by 건영
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def blog(request):
    return render(request, 'blog.html')
def contact(request):
    return render(request, 'contact.html')
def elements(request):
    return render(request, 'elements.html')
def main(request):
    return render(request, 'main.html')
def packages(request):
    return render(request, 'packages.html')
def single_blog(request):
    post = get_object_or_404(TogetherPost)
    return render(request, 'single-blog.html',{'post':post})

# def together_comment(request, post_id):
#     post = TogetherPost.objects.get(pk=post_id)

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.save()
#             return redirect('view_post', post_id=post_id)
#     else:
#         form = CommentForm()

#     return render(request, 'single-blog.html', {'form': form})

#by 건영 종료

# 로그인, 회원가입 페이지 by 문정
def user_login(request):
    # if request.method == 'POST':
    #     form = AuthenticationForm(request=request, data=request.POST)
    #     if form.is_valid():
    #         login(request, form.get_user())
    #         return redirect('trip:main')  # 로그인 성공 시 리디렉션할 페이지
    # else:
    #     form = AuthenticationForm()
    # return render(request, 'login.html', {'form': form})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request,'main.html')
    #     else:
    #         return render(request,'login.html', {'error':'username or password is incorrect'})
    # else:
    return render(request,'login.html')



def user_logout(request):
    redirect('trip:main')

def register(request):
    # return render(request, 'register.html')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('trip:main')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})


# 챗봇 BY 영민
def chatapi(request, question):
    with open('../config.json', 'r') as f:
        json_data = json.load(f)
    api_key = json_data['OPENAI_KEY']
                
    response_generator = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
            "role": "system",
            "content": "너는 우리 트립웹에 Trip봇이야. 답변은 400자 내로 깔끔하게"},
            {"role": "user", "content": f"'{question}'"},
        ],
        temperature=0.5,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        api_key=api_key,
    )
    content = response_generator['choices'][0]['message']['content']
    answer = {'answer':content}
    return JsonResponse(answer)

def chatbot(request):
    return render(request, 'test.html')
def packages(request):
  return render(request, 'packages.html', {'items' : Package.objects.all()})