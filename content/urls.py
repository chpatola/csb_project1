from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'content'

urlpatterns = [
    path('', views.index, name='index'),
    path('addcity', views.addcity, name='addcity'),
    path('userinput', views.userinput, name='userinput'),
    path('handleuserinput', views.handleuserinput, name='handleuserinput'),
    path('mlmodel', views.machinelearning, name='machinelearning'),
    path('login/', LoginView.as_view(template_name='content/login.html')),
	path('logout/', LogoutView.as_view(next_page='/')),
    path('fail', views.fail, name='fail'),
]