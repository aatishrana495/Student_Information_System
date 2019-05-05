from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta, date

sex_choice = (
	('Male', 'Male'),
	('Female', 'Female')
)

class User(AbstractUser):
	@property
	def is_student(self):
		if hasattr(self, 'student'):
			return True
		return False

	@property
	def is_teacher(self):
		if hasattr(self, 'teacher'):
			return True
		return False

class Dept(models.Model):
	id = models.CharField(primary_key=True, max_length=20)
	name = models.CharField(max_length=50)
	contact = models.BigIntegerField()

	class Meta:
		verbose_name_plural = 'Departments'

	def __str__(self):
		return self.name


class Student(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dept = models.ForeignKey(Dept, on_delete=models.CASCADE)

	id = models.CharField(primary_key=True,max_length=20)
	name = models.CharField(max_length=50)
	dob = models.DateField(default='1990-01-01',verbose_name="date of birth")
	sex = models.CharField(max_length=20, choices=sex_choice)
	contact = models.BigIntegerField()
	hostel = models.CharField(max_length=50)
	programme = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Teacher(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	dept = models.ForeignKey(Dept, on_delete=models.CASCADE)

	id = models.CharField(primary_key=True,max_length=20)
	name = models.CharField(max_length=50)
	dob = models.DateField(default='1990-01-01',verbose_name="date of birth")
	sex = models.CharField(max_length=20, choices=sex_choice)
	contact = models.BigIntegerField()
	address = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Section(models.Model):
	id = models.CharField(primary_key=True,max_length=20)
	location = models.CharField(max_length=200)

	def __str__(self):
		return self.id

class Course(models.Model):

	dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
	sections = models.ManyToManyField(Section, through='CourseSection' ,through_fields=('course','section'),)

	id = models.CharField(primary_key=True,max_length=20)
	name = models.CharField(max_length=50)
	ltp = models.CharField(max_length=20)
	credits = models.IntegerField()
	syllabus = models.TextField()

	def __str__(self):
		return self.name


class CourseSection(models.Model):

	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	section = models.ForeignKey(Section, on_delete=models.CASCADE)

	teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
	students = models.ManyToManyField(Student, through='CourseSectionStudent' ,through_fields=('coursesection','student'),)

	class Meta:
		unique_together = (('course', 'section'),)

	def __str__(self):
		return '%s : %s ' % (self.course.name, self.section.id)

class CourseSectionStudent(models.Model):

	coursesection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	mid_marks = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30)])
	end_marks = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(50)])
	ta_marks = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])

	class Meta:
		unique_together = (('coursesection', 'student'),)

	def __str__(self):
		return '%s : %s : %s ' % (self.student.name, self.coursesection.course.name, self.coursesection.section.id)

class Attendance(models.Model):

	coursesectionstudent = models.ForeignKey(CourseSectionStudent, on_delete=models.CASCADE)
	date = models.DateField(default='2019-01-01')
	status = models.BooleanField(default='True')

	class Meta:
		unique_together = (('coursesectionstudent','date'),)

	def __str__(self):
		return '%s : %s : %s : %s ' % (self.coursesectionstudent.student.name, self.coursesectionstudent.coursesection.course.name, self.coursesectionstudent.coursesection.section.id,self.date)

class Post(models.Model):

	coursesection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)

	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title

class Comment(models.Model):

	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.text


