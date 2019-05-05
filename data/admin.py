from django.contrib import admin
from .models import User,Dept,Student,Teacher,Section,Course,CourseSection
from .models import Post,Comment,CourseSectionStudent,Attendance
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Dept)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Section)
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CourseSectionStudent)
admin.site.register(Attendance)