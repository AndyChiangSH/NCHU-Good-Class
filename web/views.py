from importlib.metadata import requires
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http.response import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Avg
from .models import Department, Class, Profile, Comment, Follow
from .forms import RegisterForm, LoginForm, ProfileDeptForm
from django.core.paginator import Paginator


# 首頁
def index(request):
    num_user = User.objects.all().count()   # 使用人數
    num_class = Class.objects.all().count()  # 課程數量
    num_comment = Comment.objects.all().count()  # 評論數量

    context = {
        "num_user": num_user,
        "num_class": num_class,
        "num_comment": num_comment,
    }

    return render(request, "web/index.html", context)


# 課程清單
def class_list(request):
    # GET參數
    t = request.GET.get('t')
    q = request.GET.get('q')

    if t == None or q == None or t == "" or q == "":   # 空白查詢
        classes = Class.objects.all().order_by('id')
    else:
        if t == "id":   # 課程代碼查詢
            classes = Class.objects.filter(
                id__contains=q).order_by('id')
        elif t == "name":   # 課程名稱查詢
            classes = Class.objects.filter(
                cName__contains=q).order_by('id')
        elif t == "professor":  # 老師名稱查詢
            classes = Class.objects.filter(
                cProfessor__contains=q).order_by('id')
        elif t == "dept":   # 開課系所查詢
            classes = Class.objects.filter(
                cDept__contains=q).order_by('id')
        else:   # 未知查詢
            classes = Class.objects.none()

    # 每20堂課分成一頁
    paginator = Paginator(classes, 20)

    try:
        # 顯示當前頁數(page)
        page_number = request.GET.get('page')
        classes = paginator.get_page(page_number)
    except:
        classes = paginator.get_page(1) # 失敗則返回第一頁
    
    # 組合成課程+追蹤紀錄的列表
    class_list = list()
    for class_ in classes:
        # 取得該名使用者是否追蹤這堂課
        follow = Follow.objects.filter(fUID=request.user).filter(fCID=class_)
        if len(follow) == 0:    # 沒追蹤
            class_list.append({"class": class_, "followed": False})
        else:   # 有追蹤
            class_list.append({"class": class_, "followed": True})

    context = {
        'class_list': class_list,
        'classes': classes, # 還是有傳classes是為了要分頁
    }

    return render(request, 'web/class_list.html', context)
    

# 課程詳細內頁
def class_detail(request, code):
    # 顯示錯誤訊息
    error = "false"
    try:
        error = request.GET["error"]
    except:
        error = "false"

    # 取得課程詳細資料
    try:
        class_obj = Class.objects.get(pk=code)
    except Class.DoesNotExist:
        raise Http404('Class does not exist')
    
    # 取得該名使用者是否追蹤這堂課
    follow = Follow.objects.filter(fUID=request.user).filter(fCID=class_obj)
    followed = False
    if len(follow) == 0:    # 沒追蹤
        followed = False
    else:   # 有追蹤
        followed = True

    # 這堂課的所有評論
    comment_list = list()
    comments = Comment.objects.filter(mCID__pk=code).order_by("-mLasttime")
    try:
        for comment in comments:
            # 每個評論的使用者
            profile = Profile.objects.get(pUID=comment.mUID)
            comment_list.append({"detail": comment, "dept": profile.pDept})
    except Profile.DoesNotExist:
        raise Http404('Profile does not exist')

    context = {
        "class": class_obj,
        "comments": comment_list,
        "error": error,
        "followed": followed,
    }

    return render(request, "web/class_detail.html", context)


# 註冊
def register(request):
    error = False
    error_msg = ""
    # 註冊表單
    form = RegisterForm()

    if request.method == "POST":    # POST
        username = request.POST["username"]
        if str(username).endswith('@gmail.com'):    # gmail結尾
            form = RegisterForm(request.POST)
            if form.is_valid():     # 有效輸入
                # 儲存使用者
                form.save()
                # 預設系所為不公開
                user = User.objects.get(username=request.POST["username"])
                dept = Department.objects.get(dDept="不公開")
                # 新增profile
                Profile.objects.create(pUID=user, pDept=dept)

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


# 登入
def log_in(request):
    # 已經登入則重新導向到首頁
    if request.user.is_authenticated:
        return redirect('/')

    # 登入表單
    form = LoginForm()

    error = False
    if request.method == "POST":
        # POST資料
        username = request.POST["username"]
        password = request.POST["password"]
        next = request.POST["next"]
        # 使用者認證
        user = authenticate(username=username, password=password)
        if user != None and user.is_active:  # 認證+是否可登入
            # 登入
            login(request, user)

            return redirect(next)
        else:
            error = True
    else:
        # 取得next參數
        try:
            next = request.GET['next']
        except:
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
    # 登出
    logout(request)

    # 取得next參數
    try:
        next = request.GET['next']
    except:
        next = "/"

    return redirect(next)


# 個人資料頁面
@login_required(login_url="login")
def profile(request, id):
    # id為空
    if id == None:
        raise Http404('id can not be empty.')

    # 認證使用者是否相同
    user_id = request.user.id
    if int(user_id) != id:
        return redirect("/web/no_premission")

    # 使用者系所
    profile_dept = Profile.objects.get(pUID__id=user_id)

    context = {
        "profile_dept": profile_dept
    }

    return render(request, 'web/profile.html', context)


# 修改個人資料
@login_required(login_url="login")
def profile_edit(request, id):
    # id為空
    if id == None:
        raise Http404('id can not be empty.')

    # 認證使用者是否相同
    user = request.user
    if int(user.id) != id:
        return redirect("/web/no_premission")

    # 使用者系所
    user_obj = Profile.objects.get(pUID__id=user.id)
    # 使用者系所表單
    form = ProfileDeptForm(initial={'dept': user_obj.pDept})

    if request.method == "POST":
        # 儲存使用者回傳的系所
        form_dept = request.POST["dept"]    # 回傳的系所名稱
        dept_obj = Department.objects.get(id=form_dept)  # 取得對應的系所物件
        user_obj.pDept = dept_obj   # 修改系所
        user_obj.save()  # 儲存

        return redirect(f"/web/profile/{user.id}")

    context = {
        "form": form
    }

    return render(request, 'web/profile_edit.html', context)


# 個人評論清單
@login_required(login_url="login")
def profile_comment_list(request, id):
    # id為空
    if id == None:
        raise Http404('id can not be empty.')

    # 認證使用者是否相同
    user = request.user
    if str(user.id) != str(id):
        return redirect("/web/no_premission")

    # 該使用者的所有評論(新的排在前面)
    comments = Comment.objects.filter(mUID=user).order_by("-mLasttime")

    context = {
        "comments": comments,
    }

    return render(request, 'web/profile_comment_list.html', context)


# 個人追蹤清單
@login_required(login_url="login")
def profile_follow_list(request, id):
    # id為空
    if id == None:
        raise Http404('id can not be empty.')

    # 認證使用者是否相同
    user = request.user
    if str(user.id) != str(id):
        return redirect("/web/no_premission")

    # 該使用者的所有追蹤(新的排在前面)
    follows = Follow.objects.filter(fUID=user).order_by("-fLasttime")

    context = {
        "follows": follows,
    }

    return render(request, 'web/profile_follow_list.html', context)


# 確認數字範圍(0~10)
def check_number(num):
    if num != None:
        if int(num) >= 0 and int(num) <= 10:
            return True
    return False

# 確認字串長度(10~1000)
def check_string(string):
    if len(string) > 1000 or len(string) < 10:
        return False
    else:
        return True


# 更新評分平均
def update_avg(class_):
    # 取得甜、涼、有趣、學習、參與的平均
    new_avgs = Comment.objects.filter(mCID=class_).aggregate(
        Avg('mCool'), Avg('mSweet'), Avg('mFun'), Avg('mLearn'), Avg('mJoin'))

    # 取得平均
    new_avg_cool = new_avgs['mCool__avg']
    new_avg_sweet = new_avgs['mSweet__avg']
    new_avg_fun = new_avgs['mFun__avg']
    new_avg_learn = new_avgs['mLearn__avg']
    new_avg_join = new_avgs['mJoin__avg']

    # 平均如果是None，則設為0
    if new_avg_cool == None:
        new_avg_cool = 0
    if new_avg_sweet == None:
        new_avg_sweet = 0
    if new_avg_fun == None:
        new_avg_fun = 0
    if new_avg_learn == None:
        new_avg_learn = 0
    if new_avg_join == None:
        new_avg_join = 0

    # 更新課程平均
    class_.cCool = new_avg_cool
    class_.cSweet = new_avg_sweet
    class_.cFun = new_avg_fun
    class_.cLearn = new_avg_learn
    class_.cJoin = new_avg_join

    # 存檔
    class_.save()


# 新增評論
@login_required(login_url="login")
def comment_create(request, code):
    # code不得為空
    if code == None:
        raise Http404('code can not be empty.')

    # 使用者ID
    user_id = request.user.id

    # 取得該堂課程和該名使用者
    try:
        class_ = Class.objects.get(id=code)
        user = User.objects.get(id=user_id)
    except Class.DoesNotExist:
        raise Http404('Class does not exist')

    # 取得該堂課程和該名使用者的評論
    comments = Comment.objects.filter(mCID=class_).filter(mUID=user)

    # 是否已經存在評論
    if len(comments) == 0:
        if request.method == "POST":
            # 取得POST資料
            cool = request.POST["cool"]
            sweet = request.POST["sweet"]
            fun = request.POST["fun"]
            learn = request.POST["learn"]
            join = request.POST["join"]
            content = request.POST["content"]
            lasttime = timezone.now()

            # 驗證評分和評論是否合法
            if check_number(cool) and check_number(sweet) and check_number(fun) and check_number(learn) and check_number(join) and check_string(content):
                # 新增評論
                row = Comment.objects.create(
                    mCID=class_,
                    mUID=user,
                    mCool=int(cool),
                    mSweet=int(sweet),
                    mFun=int(fun),
                    mLearn=int(learn),
                    mJoin=int(join),
                    mContent=content,
                    mLasttime=lasttime
                )
                row.save()
                # 更新平均
                update_avg(class_)

                return redirect(f"/web/class/{code}")

        return render(request, 'web/comment_create.html')
    else:
        return redirect(f"/web/class/{code}/?error=true")


# 編輯評論
@login_required(login_url="login")
def comment_edit(request, id=None):
    # id不得為空
    if id == None:
        raise Http404('id can not be empty.')

    # 評論是否存在
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise Http404('Comment does not exist')

    # 該名使用者
    user = request.user
    # 認證使用者是否相同
    if user.id != comment.mUID.id:
        return redirect("/web/no_premission")

    if request.method == "POST":
        # 取得POST資料
        cool = request.POST["cool"]
        sweet = request.POST["sweet"]
        fun = request.POST["fun"]
        learn = request.POST["learn"]
        join = request.POST["join"]
        content = str(request.POST["content"])
        next = request.POST["next"]

        # 驗證評分和評論是否合法
        if check_number(cool) and check_number(sweet) and check_number(fun) and check_number(learn) and check_number(join) and check_string(content):
            # 修改資料
            comment.mCool = int(cool)
            comment.mSweet = int(sweet)
            comment.mFun = int(fun)
            comment.mLearn = int(learn)
            comment.mJoin = int(join)
            comment.mContent = content
            comment.save()
            # 更新平均
            update_avg(comment.mCID)

            return redirect(next)
    else:
        # GET參數
        try:
            next = request.GET["next"]
        except:
            next = "/"

    context = {
        "comment": comment.__dict__,
        "next": next,
    }

    return render(request, 'web/comment_edit.html', context)


# 刪除評論
@login_required(login_url="login")
def comment_delete(request, id=None):
    # id不得為空
    if id == None:
        raise Http404('id can not be empty.')

    # 評論是否存在
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise Http404('Comment does not exist')

    # 驗證使用者是否相同
    user = request.user
    if user.id != comment.mUID.id:
        return redirect("/web/no_premission")

    if request.method == "POST":
        next = request.POST["next"]
        # 刪除資料
        comment.delete()
        # 更新平均
        update_avg(comment.mCID)

        return redirect(next)
    else:
        # 取得next
        try:
            next = request.GET["next"]
        except:
            next = "/"

        context = {
            "next": next,
        }

        return render(request, 'web/comment_delete.html', context)


# 沒有權限
def no_premission(request):
    return render(request, 'web/no_premission.html')


# 追蹤(星號)
@login_required(login_url="login")
def follow(request, id=None):
    if request.method == "POST":
        user = request.user     # 當前使用者
        next = "/"
        if request.POST["next"] != None:
            next = request.POST["next"]     # 原本的位置

        if id == None or id == "":  # id為空
            raise Http404('Class can not be empty.')
        else:
            try:
                class_obj = Class.objects.get(id=id)    # 取得該堂課程
            except:
                raise Http404('Class does not exist.')

            # 取得追蹤紀錄
            follow = Follow.objects.filter(fUID=user).filter(fCID=class_obj)
            if len(follow) == 0:    # 沒追蹤則新增
                new_follow = Follow.objects.create(
                    fUID=user,
                    fCID=class_obj,
                )
                new_follow.save()
            else:   # 有追蹤則刪除
                follow.delete()

            return redirect(next)   # 返回原本的位置
    else:
        raise Http404('GET method not allow.')