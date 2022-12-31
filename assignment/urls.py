from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('assignment/',views.assignment,name='assignment'),
    path('assignment_view/',views.assignment_view,name='assignment_view'),
    path('assignment_submit/',views.assignmentsubmit,name='assignment_submit'),
    path('assignmentupdate/<int:a_id>',views.assignmentupdate,name="assignmentupdate"),
    path('assignmentdelete/<int:a_id>',views.assignmentdelete,name="assignmentdelete"),
    path('assignment_mark',views.assignment_mark,name="assignment_mark"),


    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)