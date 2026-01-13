from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, home, login, about, create_task, delete_task, update_task,assignment_task,update_task_status,personal_area

urlpatterns = [
path("register/",register,name="register"),
path("login/",login,name="login"),
path("personal_area/",personal_area,name="personal_area"),
path("logout/",auth_views.LogoutView.as_view(),name="logout"),
path("home/",home,name="home"),
path("", about),
path("tasks/create/", create_task, name="create_task"),
path("tasks/delete/<int:task_id>", delete_task, name="delete_task"),
path("tasks/update/<int:task_id>", update_task, name="update_task"),
path("tasks/assignment/<int:task_id>",assignment_task, name="assignment_task"),
path("tasks/update_status/<int:task_id>",update_task_status, name="update_task_status"),

]

