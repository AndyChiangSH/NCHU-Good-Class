from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),    # 首頁
    path('class/', views.class_list, name="class_list"), # 課程清單
    path('class/<str:id>/', views.class_detail, name='class_detail'),   # 課程詳細頁面
    path('register/', views.register, name="register"), # 註冊
    path('login/', views.log_in, name="login"),     # 登入
    path('logout/', views.log_out, name="logout"),  # 登出
    path('profile/', views.profile, name="profile"),   # 個人資料
    path('profile/edit/', views.profile_edit, name="profile_edit"),    # 編輯個人資料
    path('profile/comments/', views.profile_comment_list, name="profile_comment_list"),    # 個人評論清單
    path('profile/follows/', views.profile_follow_list, name="profile_follow_list"),    # 個人評論清單
    path('comment/create/<str:id>', views.comment_create, name="comment_create"),     # 新增評論
    path('comment/edit/<int:id>', views.comment_edit, name="comment_edit"),     # 編輯評論
    path('comment/delete/<int:id>', views.comment_delete, name="comment_delete"),   # 刪除評論
    path('no_premission/', views.no_premission, name="no_premission"),   # 沒有權限
    path('follow/<str:id>', views.follow, name="follow"),    # 追蹤
]
