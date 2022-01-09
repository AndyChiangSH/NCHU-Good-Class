from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Department, Class, Profile, Comment
from django.views import generic
from django.http.response import Http404


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
    try:
        class_ = Class.objects.get(pk=pk)
    except Class.DoesNotExist:
        raise Http404('Class does not exist')

    comment_list = []
    comments = Comment.objects.filter(mCID__pk=pk)
    for comment in comments:
        profile = Profile.objects.get(pUID=comment.mUID)
        comment_list.append({"detail": comment, "dept": profile.pDept})

    context = {
        "class": class_,
        "comments": comment_list
    }

    return render(request, "web/class_detail.html", context)