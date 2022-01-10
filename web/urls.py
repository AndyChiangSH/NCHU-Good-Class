from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('classes/', views.ClassListView.as_view(), name="class_list"),
    path('class/<str:pk>/', views.class_detail, name='class_detail'),
    path('register/', views.register, name="register"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('user/<int:pk>', views.profile, name="profile"),
    path('user/<int:pk>/edit', views.profile_edit, name="profile_edit"),
    path('user/<int:pk>/list', views.profile_comment_list, name="profile_comment_list"),
    path('comment/create/<str:code>', views.comment_create, name="comment_create"),
    path('comment/edit/<int:pk>', views.comment_edit, name="comment_edit"),
    path('comment/delete/<int:pk>', views.comment_delete, name="comment_delete"),
    path('no_premission', views.no_premission, name="no_premission"),
]
