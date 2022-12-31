from django.core.checks import messages
from django.shortcuts import render,redirect
from .models import *
from .forms import *

from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def assignment(request):
    if request.method=='POST':
        form=AssignmentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('assignment_view')
        else:
            return HttpResponse('not valid')
    else:
        form=AssignmentForm()
    return render(request,'assignment.html',{'form':form})

def assignment_view(request):
    assignment=Assignment.objects.all()
    return render(request,'assignment_view.html',{'assignment':assignment})


def assignmentsubmit(request):
    if request.method=='POST':
        aname=request.POST.get('aname')
        ans=request.FILES.get('ans')

        AssignmentSubmit.objects.create(
            user=request.user,
            assignment=aname,
            assignment_ans=ans
        )
        return redirect('assignment_view')
    return render(request,'assignment_submit.html')

def assignmentupdate(request,a_id):
    ass=AssignmentSubmit.objects.get(id=a_id)
    form=AssignmentSubmitForm(instance=ass)
    if request.method=='POST':
        form=AssignmentSubmitForm(request.POST,instance=ass)
        form.save()
        return redirect('assignment_view')
    return render(request,'assignment_update.html',{'form':form})

def assignmentdelete(request,a_id):
    deleteitem=AssignmentSubmit.objects.get(id=a_id)
    deleteitem.delete()
    return redirect('assignment_view')

def assignment_mark(request):
    mark=AssignmentSubmit.objects.all()
    return render(request,'assignment_mark.html',{'mark':mark})

