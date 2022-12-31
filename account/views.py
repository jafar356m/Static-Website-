from django.forms.models import ALL_FIELDS
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import date, timedelta
from exam import models as QMODEL
from .models import *
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request,'home.html')



def register(request):
    registered = False

    if request.method == 'POST':
        user_form = Userform(data = request.POST)
        profile_form = UserProfileInfoform(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            registered  = True
            
        else:
            print(user_form.errors,profile_form.errors)


    else :
        user_form = Userform()
        profile_form = UserProfileInfoform()

    return render(request,'register.html',{'registered' : registered ,'user_form':user_form,'profile_form':profile_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account Is Deactivated')

        else : 
            return HttpResponse('please check username and password')
    else:
        return render(request,'index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def student_exam_view(request):
    courses=QMODEL.ExamSubject.objects.all()
    return render(request,'student_exam.html',{'courses':courses})


def take_exam_view(request,pk):
    course=QMODEL.ExamSubject.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
   
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks 
    
    return render(request,'take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})


def start_exam_view(request,pk):
    course=QMODEL.ExamSubject.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    response= render(request,'start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response



def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.ExamSubject.objects.get(id=course_id)
        
        total_marks=0
        count=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = User_Profile.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.exam=course
        result.student=student
        if total_marks < (course.total_marks/2):
            result.status='FAIL'
        else:
            result.status='PASS' 

        
        vs=result.status
        a=str(vs)
        result.as_pa=a
        print(a)
        result.save()    
        
        return HttpResponseRedirect('view-result')





def view_result_view(request):
    courses=QMODEL.ExamSubject.objects.all()
    return render(request,'view_result.html',{'courses':courses})
    


def check_marks_view(request,pk):
    course=QMODEL.ExamSubject.objects.get(id=pk)
    student = User_Profile.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'check_marks.html',{'results':results})

def student_marks_view(request):
    courses=QMODEL.ExamSubject.objects.all()
    return render(request,'student_marks.html',{'courses':courses})

def all_mark(request):
    results=QMODEL.Result.objects.all()
    return render(request,'view_student_mark.html',{'results':results})
  
def contact(request):
	if request.method == "POST":
		name = request.POST.get('name')
		print(name)
		email = request.POST.get('email')
		print(email)
		content = request.POST.get('content')
          
		Contact.objects.create(
			name = name,
			email= email,
			content = content)
		return render(request,'contact.html',{'msg':'Details Successfully Saved.'})
   
	else :
		return render(request,'contact.html',{})


def review(request):
    if request.method=="POST":
        student=request.POST.get('student')
        review=request.POST.get('review')
       
        StudentReview.objects.create(
            student=student,
            review=review,
        )
    return render(request,'review.html')


def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            messages.success(request,"YOUR PASSWORD SUCCEFULLY UPDATED")
            return render(request,'change_password.html')
        else:
            messages.error(request,'PLEASE CORRECT ERROR')
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'change_password.html',{'form':form})

def view_review(request):
    review=StudentReview.objects.all()
    return render(request,'view_review.html',{'review':review})
