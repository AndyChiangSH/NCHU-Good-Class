from django.contrib import admin
from .models import Department, Class, Profile, Comment
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'dDept')

class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('id', 'dDept')
    search_fields = ('dDept', )
    ordering = ('dDept', 'id')

admin.site.register(Department, DepartmentAdmin)


class ClassResource(resources.ModelResource):
    class Meta:
        model = Class
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'cName', 'cEn_name', 'cProfessor', 'cDept', 'cType', 'cCredit', 'cLang')

class ClassAdmin(ImportExportModelAdmin):
    resource_class = ClassResource
    list_display = ('id', 'cName', 'cEn_name', 'cProfessor', 'cDept', 'cType', 'cCredit', 'cLang')
    search_fields = ('id', 'cName', 'cEn_name', 'cProfessor', 'cDept', 'cType', 'cCredit', 'cLang')
    ordering = ('id', )

admin.site.register(Class, ClassAdmin)


class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    list_display = ('id', 'pUID', 'pDept')
    search_fields = ('id', 'pUID', 'pDept')
    ordering = ('id', )

admin.site.register(Profile, ProfileAdmin)


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment

class CommentAdmin(ImportExportModelAdmin):
    resource_class = CommentResource
    list_display = ('id', 'mUID', 'mCID', 'mLasttime')
    search_fields = ('id', 'mUID', 'mCID')
    ordering = ('-mLasttime', 'id')

admin.site.register(Comment, CommentAdmin)