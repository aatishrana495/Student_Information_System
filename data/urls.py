from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student/<slug:id>/',views.student,name='student'),
    path('teacher/<slug:id>/',views.teacher,name='teacher'),
    path('student/<slug:id>/courses/',views.scourses,name='scourses'),
    path('teacher/<slug:id>/courses/',views.tcourses,name='tcourses'),
    path('blog/<int:id>/',views.blog,name='blog'),
    path('post/<int:num>/edit/<int:id>',views.post_edit,name='post_edit'),
    path('post/<int:id>/new/',views.post_new,name='post_new'),
    path('post/<int:num>/delete/<int:id>',views.post_delete,name='post_delete'),
    path('comment/<int:num>/add_comment/<int:id>',views.add_comment,name='add_comment'),
    path('comment/<int:num>/delete_comment/<int:id>',views.delete_comment,name='delete_comment'),
    path('teacher/<slug:id>/attendance/',views.t_attendance,name='t_attendance'),
    path('sub/<int:id>/attendance/',views.sub_attendance,name='sub_attendance'),
]
