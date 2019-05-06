from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Dept,Student,Teacher,Section,Course,CourseSection
from .models import Post,Comment,CourseSectionStudent,Attendance
from .forms import PostForm,CommentForm,DateForm

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
	ddl = Attendance.objects.filter(coursesectionstudent__coursesection__pk=id).values('date').distinct()
	cso = CourseSection.objects.get(pk=id)
	return render(request,'data/sub_attendance.html',{'ddl':ddl,'cso':cso,'id':id})

@login_required
def all_students(request,id,date):
	ao = Attendance.objects.filter(coursesectionstudent__coursesection__pk=id,date=date)
	return render(request,'data/all_students.html',{'ao':ao,'id':id})

@login_required
def change_attendance(request,id):
	a = Attendance.objects.get(pk=id)
	if a.status:
		a.status=False
		a.save()
	else:
		a.status=True
		a.save()
	return redirect('all_students',a.coursesectionstudent.coursesection.pk,a.date)

@login_required
def add_date(request,id):
	if request.method=="POST":
		form=DateForm(request.POST)
		if form.is_valid():
			csso=CourseSectionStudent.objects.filter(coursesection__pk=id)
			for css in csso:
				a=Attendance.objects.create(coursesectionstudent=css,date=form.cleaned_data['date'])
				a.save()
			return redirect('sub_attendance',id)
	else:
		form=DateForm()
	return render(request,'data/add_date.html',{ 'form':form })

@login_required
def s_attendance(request,id):
	so = get_object_or_404(Student,pk=id)
	subs = so.coursesection_set.all()
	return render(request,'data/s_attendance.html',{'subs':subs})

@login_required
def all_dates(request,id):
	ao = Attendance.objects.filter(coursesectionstudent__coursesection__pk=id,coursesectionstudent__student__pk=request.user.student.id)
	cso = CourseSection.objects.get(pk=id)
	total=0
	attended=0
	for a in ao:
		total=total+1
		if a.status:
			attended=attended+1
	return render(request,'data/all_dates.html',{'ao':ao,'cso':cso,'total':total,'attended':attended})

@login_required
def t_marks(request,id):
	to = get_object_or_404(Teacher,pk=id)
	subs = to.coursesection_set.all()
	return render(request,'data/t_marks.html',{'subs':subs})

@login_required
def sub_marks(request,id):
	csso = CourseSectionStudent.objects.filter(coursesection__pk=id)
	return render(request,'data/sub_marks.html',{ 'csso':csso,'id':id })

@login_required
def edit_marks(request,id,num):
	csso = CourseSectionStudent.objects.filter(coursesection__pk=id)
	return render(request,'data/edit_marks.html',{ 'csso':csso,'id':id,'num':num })

@login_required
def submit_marks(request,id,num):
	csso = CourseSectionStudent.objects.filter(coursesection__pk=id)
	for css in csso:
		if num==1:
			css.mid_marks=request.POST[css.student.id]
			css.save()
		elif num==2:
			css.end_marks=request.POST[css.student.id]
			css.save()
		else:
			css.ta_marks=request.POST[css.student.id]
			css.save()
	return render(request,'data/sub_marks.html',{ 'csso':csso,'id':id })

@login_required
def s_marks(request,id):
	so = get_object_or_404(Student,pk=id)
	csso = so.coursesectionstudent_set.all()
	return render(request,'data/s_marks.html',{'csso':csso})