from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Dept,Student,Teacher,Section,Course,CourseSection
from .models import Post,Comment,CourseSectionStudent,Attendance
from .forms import PostForm,CommentForm

@login_required
def index(request):
	if request.user.is_superuser:
		return redirect('http://127.0.0.1:8000/admin')
	if request.user.is_student:
		return redirect('student',id=request.user.student.id)
	if request.user.is_teacher:
		return redirect('teacher',id=request.user.teacher.id)
	return redirect('logout')


@login_required
def student(request,id):
	so = get_object_or_404(Student,pk=id)
	return render(request,'data/student.html',{'so':so})

@login_required
def teacher(request,id):
	to = get_object_or_404(Teacher,pk=id)
	return render(request,'data/teacher.html',{'to':to})

@login_required
def scourses(request,id):
	so = get_object_or_404(Student,pk=id)
	subs = so.coursesection_set.all()
	return render(request,'data/scourses.html',{'subs':subs})

@login_required
def tcourses(request,id):
	to = get_object_or_404(Teacher,pk=id)
	subs = to.coursesection_set.all()
	return render(request,'data/tcourses.html',{'subs':subs})

@login_required
def blog(request,id):
	cso = get_object_or_404(CourseSection,pk=id)
	return render(request,'data/blog.html',{'cso':cso})

@login_required
def post_edit(request,id,num):
	post=get_object_or_404(Post,pk=id)
	if request.method=="POST":
		form=PostForm(request.POST,instance=post)
		if form.is_valid():
			post=form.save(commit=False)
			post.coursesection=get_object_or_404(CourseSection,pk=num)
			post.save()
			return redirect('blog',num)
	else:
		form=PostForm(instance=post)
	return render(request,'data/post_edit.html',{ 'form':form })

@login_required
def post_new(request,id):
	if request.method=="POST":
		form=PostForm(request.POST)
		if form.is_valid():
			post=form.save(commit=False)
			post.coursesection=get_object_or_404(CourseSection,pk=id)
			post.save()
			return redirect('blog',id)
	else:
		form=PostForm()
	return render(request,'data/post_edit.html',{ 'form':form })

@login_required
def post_delete(request,num,id):
	post=get_object_or_404(Post,pk=id)
	post.delete()
	return redirect('blog',num)


@login_required
def add_comment(request,id,num):
	post=get_object_or_404(Post,pk=id)
	if request.method=="POST":
		form=CommentForm(request.POST)
		if form.is_valid():
			comment=form.save(commit=False)
			comment.post=post
			comment.author=request.user
			comment.save()
			return redirect('blog',num)
	else:
		form=CommentForm()
	return render(request,'data/add_comment.html',{ 'form':form })

@login_required
def delete_comment(request,num,id):
	comment=get_object_or_404(Comment,pk=id)
	comment.delete()
	return redirect('blog',num)

@login_required
def t_attendance(request,id):
	to = get_object_or_404(Teacher,pk=id)
	subs = to.coursesection_set.all()
	return render(request,'data/t_attendance.html',{'subs':subs})

@login_required
def sub_attendance(request,id):
	to = get_object_or_404(Teacher,pk=id)
	subs = to.coursesection_set.all()
	return render(request,'data/t_attendance.html',{'subs':subs})