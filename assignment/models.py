from django.db import models
from cariculam.models import Course
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Assignment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,blank=True,null=True)
    title=models.CharField(max_length=30)
    assignment_question=models.FileField(upload_to='assignment_questions',blank=True,null=True)
    assignment_mark=models.PositiveIntegerField(blank=True,null=True)
    date_created=models.DateTimeField(default=timezone.now)
    last_date_submit=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return str(self.course)


class AssignmentSubmit(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    assignment=models.CharField(max_length=100)
    assignment_ans=models.FileField(upload_to='assinment_ans',blank=True,null=True)
    date_created=models.DateTimeField(default=timezone.now)
    assignment_mark=models.PositiveIntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.user)






