from django.http.response import HttpResponse
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
    template_name = "web/classes.html"
    paginate_by = 20
    order_dy = ('code')

    def get_queryset(self):
        t = self.request.GET.get('t')
        q = self.request.GET.get('q')

        print(t)
        print(q)

        object_list = self.model.objects.none()

        if t == None or q == None or q == "":
            object_list = self.model.objects.all()
        else:
            if t == "code":
                object_list = self.model.objects.filter(cCode__contains=q)
            elif t == "name":
                object_list = self.model.objects.filter(cName__contains=q)
            elif t == "professor":
                object_list = self.model.objects.filter(cProfessor__contains=q)
            elif t == "dept":
                object_list = self.model.objects.filter(cDept__contains=q)

        return object_list