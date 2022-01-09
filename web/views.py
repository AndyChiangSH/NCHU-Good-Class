from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Department, Class, Profile, Comment
from django.views import generic
from django.http.response import Http404
from .forms import RegisterForm, LoginForm, ProfileDeptForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Create your views here.
def index(request):
    
    num_user = User.objects.all().count()
    num_class = Class.objects.all().count()
    num_comment = Comment.objects.all().count()

    context = {
        "num_user": num_user,
        "num_class": num_class,
        "num_comment": num_comment,
    }

    return render(request, "web/index.html", context)


class ClassListView(generic.ListView):
    model = Class
    template_name = "web/class_list.html"
    paginate_by = 20
    order_dy = ('id')

    def get_queryset(self):
        t = self.request.GET.get('t')
        q = self.request.GET.get('q')
        # print(t)
        # print(q)

        if t == None or q == None or q == "":
            object_list = self.model.objects.all()
        else:
            if t == "id":
                object_list = self.model.objects.filter(id__contains=q)
            elif t == "name":
                object_list = self.model.objects.filter(cName__contains=q)
            elif t == "professor":
                object_list = self.model.objects.filter(cProfessor__contains=q)
            elif t == "dept":
                object_list = self.model.objects.filter(cDept__contains=q)
            else:
                object_list = self.model.objects.none()

        return object_list


def class_detail_view(request, pk):
    error = "t"
    try:
        error = request.GET["error"]
    except:
        error = "f"

    try:
        class_ = Class.objects.get(pk=pk)
    except Class.DoesNotExist:
        raise Http404('Class does not exist')

    comment_list = []
    comments = Comment.objects.filter(mCID__pk=pk).order_by("-mLasttime")
    try:
        for comment in comments:
            profile = Profile.objects.get(pUID=comment.mUID)
            comment_list.append({"detail": comment, "dept": profile.pDept, "mUID": comment.mUID.id})
    except Profile.DoesNotExist:
        raise Http404('Profile does not exist')

    context = {
        "class": class_,
        "comments": comment_list,
        "error": error,
    }

    return render(request, "web/class_detail.html", context)


# 註冊
def register(request):
    form = RegisterForm()
    error = False
    error_msg = ""

    if request.method == "POST":
        username = request.POST["username"]
        if str(username).endswith('@gmail.com'):
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = User.objects.get(username=request.POST["username"])
                Profile.objects.create(pUID=user, pDept=None)
                return redirect('/web/login')
            else:
                error = True
                error_msg = "電子信箱或密碼不符合規定!"
        else:
            error = True
            error_msg = "電子信箱必須為gmail.com結尾!"
    
    context = {
        'form': form,
        'error': error,
        'error_msg': error_msg,
    }

    return render(request, 'web/register.html', context)


#登入
def log_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    error = False

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        next = request.POST["next"]
        user = authenticate(username=username, password=password)
        if user != None and user.is_active:
            login(request, user)
            return redirect(next)
        else:
            error = True
    else:
        if len(request.GET) != 0:
            next = request.GET['next']
        else:
            next = "/"
        
    context = {
        'form': form,
        'error': error,
        'next': next,
    }

    return render(request, 'web/login.html', context)


# 登出
@login_required(login_url="login")
def log_out(request):
    logout(request)

    next = "/"
    if len(request.GET) != 0:
        next = request.GET["next"]

    return redirect(next)


# 個人資料頁面
@login_required(login_url="login")
def profile(request, pk):
    user_id = request.user.id
    if str(user_id) != str(pk) or pk == None:
        return redirect("/")
    
    profile_dept = Profile.objects.get(pUID__id=user_id)

    context = {
        "profile_dept": profile_dept
    }
    
    return render(request, 'web/profile.html', context)


# 修改個人資料
@login_required(login_url="login")
def profile_edit(request, pk):
    user_id = request.user.id
    if str(user_id) != str(pk) or pk == None:
        return redirect("/")

    form = ProfileDeptForm()

    if request.method == "POST":
        profile_dept = Profile.objects.get(pUID__id=user_id)
        dept = request.POST["dept"]
        dept_obj = Department.objects.get(id=dept)
        profile_dept.pDept = dept_obj
        profile_dept.save()
        return redirect(f"/web/user/{user_id}")

    context = {
        "form": form
    }
    
    return render(request, 'web/profile_edit.html', context)


# 個人評論清單
@login_required(login_url="login")
def profile_comment_list(request, pk):
    user_id = request.user.id
    if str(user_id) != str(pk) or pk == None:
        return redirect("/")
    
    comments = Comment.objects.filter(mUID=request.user).order_by("-mLasttime")
    print(comments)

    context = {
        "comments": comments,
    }

    return render(request, 'web/profile_comment_list.html', context)


def check_number_range(num):
    if num > 10 or num < 0:
        return False
    else:
        return True

def check_string_range(string):
    if len(string) > 1000 or len(string) < 10:
        return False
    else:
        return True

# 新增評論
@login_required(login_url="login")
def comment_create(request, code):
    print(code)
    user_id = request.user.id

    try:
        class_ = Class.objects.get(id=code)
        user = User.objects.get(id=user_id)
    except Class.DoesNotExist:
        raise Http404('Class does not exist')
    
    comments = Comment.objects.filter(mCID=class_).filter(mUID=user)
    print(comments)

    if len(comments) == 0:
        if request.method == "POST":
            cool = int(request.POST["cool"])
            sweet = int(request.POST["sweet"])
            fun = int(request.POST["fun"])
            learn = int(request.POST["learn"])
            join = int(request.POST["join"])
            content = str(request.POST["content"])
            lasttime = timezone.now()

            if check_number_range(cool) and check_number_range(sweet) and check_number_range(fun) and check_number_range(learn) and check_number_range(join) and check_string_range(content):
                row = Comment.objects.create(
                    mCID=class_, 
                    mUID=user, 
                    mCool=cool,
                    mSweet=sweet,
                    mFun=fun, 
                    mLearn=learn, 
                    mJoin=join, 
                    mContent=content, 
                    mLasttime=lasttime
                )
                row.save()
                print("create!")

            return redirect(f"/web/class/{code}")
        else:
            return render(request, 'web/comment_create.html')
    else:
        print("repeat!")
        return redirect(f"/web/class/{code}/?error=t")
    
    