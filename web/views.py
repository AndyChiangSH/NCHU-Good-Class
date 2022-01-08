from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Department, Class, Profile, Comment
from django.views import generic


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
    paginate_by = 20