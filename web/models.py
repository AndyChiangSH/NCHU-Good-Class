from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    dDept = models.CharField("系所名稱", max_length=50, unique=True)

    def __str__(self):
        return self.dDept


class Class(models.Model):
    id = models.CharField("課程代碼", max_length=4, primary_key=True)
    cName = models.CharField("課程中文名稱", max_length=50)
    cEn_name = models.CharField("課程英文名稱", max_length=100, null=True)
    cProfessor = models.CharField("課程教師", max_length=50)
    cDept = models.CharField("課程系所", max_length=50)
    cType = models.CharField("課程類別", max_length=2)
    cCredit = models.DecimalField("課程學分", max_digits=1, decimal_places=0, default=0)
    cLang = models.CharField("課程語言", max_length=2)
    cCool = models.DecimalField("涼", max_digits=3, decimal_places=1, default=0)
    cSweet = models.DecimalField("甜", max_digits=3, decimal_places=1, default=0)
    cFun = models.DecimalField("有趣", max_digits=3, decimal_places=1, default=0)
    cLearn = models.DecimalField("學習", max_digits=3, decimal_places=1, default=0)
    cJoin = models.DecimalField("參與", max_digits=3, decimal_places=1, default=0)

    def __str__(self):
        return self.cName


class Profile(models.Model):
    pUID = models.OneToOneField(to=User, on_delete=models.CASCADE)
    pDept = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.pUID)


class Comment(models.Model):
    mUID  = models.ForeignKey(to=User, on_delete=models.CASCADE)
    mCID = models.ForeignKey(to=Class, on_delete=models.CASCADE)
    mContent = models.TextField("評論內容", max_length=1000)
    mCool = models.DecimalField("涼", max_digits=2, decimal_places=0, default=0)
    mSweet = models.DecimalField("甜", max_digits=2, decimal_places=0, default=0)
    mFun = models.DecimalField("有趣", max_digits=2, decimal_places=0, default=0)
    mLearn = models.DecimalField("學習", max_digits=2, decimal_places=0, default=0)
    mJoin = models.DecimalField("參與", max_digits=2, decimal_places=0, default=0)
    mLasttime = models.DateTimeField("最後修改時間", default=timezone.now)

    def __str__(self):
        return f"{self.mUID}, {self.mCID}"

    class Meta:
        unique_together = (("mUID", "mCID"),)