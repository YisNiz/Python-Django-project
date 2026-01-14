from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .form import RegisterForm, LoginForm, TaskForm, Personal_areaForm, UpdateTaskForm
from django.contrib.auth import  login as auth_login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task, Status, CustomUser, Role


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            if request.user.team is None or request.user.role is None:
               return redirect("personal_area")
            else:
               return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})



@login_required(login_url="login")
def personal_area(request):
    if request.user.team is not None and request.user.role is not None:
        messages.error(request,"כבר בחרת צוות ותפקיד אין אפשרות לשנות אלא אם כן תירשם מחדש")
        return redirect("home")

    if request.method == 'POST':
        form = Personal_areaForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = Personal_areaForm(instance=request.user)

    return render(request, 'personalArea.html', {'form': form})



@login_required(login_url="login")
def home(request):
    user = request.user

    tasks = Task.objects.filter(team=user.team)\
        if user.team else Task.objects.none()

    status_param = request.GET.get("status", "")
    worker_id = request.GET.get("worker_id")
    worker_id = int(worker_id) if worker_id else None
    if status_param:
        tasks = tasks.filter(status=status_param)
    if worker_id:
        tasks = tasks.filter(worker_id=worker_id)

    workers = CustomUser.objects.filter(team=user.team, role=Role.USER) if user.team else CustomUser.objects.none()

    is_manager = bool(user.team and user.team.admin_id == user.id)
    add_form = TaskForm()
    edit_form=UpdateTaskForm()
    return render(request, "home.html", {"tasks": tasks,"add_form": add_form,"edit_fotm":edit_form,"is_manager": is_manager,
    "workers": workers,"status_param": status_param,"worker_id": worker_id,"Status": Status,})


@login_required(login_url="login")
def create_task(request):
    if  request.user.team and request.user.team.admin_id == request.user.id:
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.created_by = request.user
                task.team = request.user.team
                task.save()
                return redirect("home")
            else:
                tasks = Task.objects.filter(team=request.user.team)
                is_manager = True
                return render(request, "home.html", {"form": form,"tasks": tasks,"is_manager": is_manager})
    else:
        messages.error(request, "אין לך הרשאה ליצור משימות לצוות זה.")
    return redirect("home")

@login_required(login_url="login")
def delete_task(request, task_id):
    if  request.user.team and request.user.team.admin_id == request.user.id:
        if request.method == "POST":
            task = get_object_or_404(Task, id=task_id, team=request.user.team)
            if task.worker is None:
                task.delete()
                return redirect("home")
            else:
                messages.error(request, "אין אפשרות למחוק משימה אשר משוייכת לעובד כבר")
    else:
        messages.error(request, "אין לך הרשאה למחוק משימות לצוות זה.")
    return redirect("home")



@login_required(login_url="login")
def update_task(request, task_id):
    if request.user.team and request.user.team.admin_id == request.user.id:
        task = get_object_or_404(Task, id=task_id, team=request.user.team)
        if request.method == "POST":
            form = UpdateTaskForm(request.POST, instance=task)
            if form.is_valid():
                if task.worker is None:
                    form.save()
                    return redirect("home")
                else:
                    messages.error(request, "אין אפשרות לעדכן משימה אשר משוייכת לעובד כבר")
                    return redirect("home")
        else:
            edit_form = UpdateTaskForm(instance=task)
            add_form = TaskForm()
        tasks = Task.objects.filter(team=request.user.team)
        is_manager = True
        return render(request, "home.html", {"edit_form": edit_form,"add_form":add_form,"tasks": tasks,"is_manager": is_manager,"edit_task": task})
    else:
        messages.error(request, "אין לך הרשאה לעדכן משימות לצוות זה.")
    return redirect("home")


@login_required(login_url="login")
def assignment_task (request, task_id):
        task = get_object_or_404(Task, id=task_id, team=request.user.team)
        if request.method == "POST":
            if task.worker is None:
                task.worker=request.user
                task.status=Status.IN_PROGRESS
                task.save(update_fields=["worker", "status"])
                return redirect("home")
            else:
                messages.error(request,"אין אפשרות לשייך משימה שכבר משויכת לעובד אחר")
        return redirect("home")




@login_required(login_url="login")
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, team=request.user.team)
    if request.method == "POST":
        if task.worker==request.user:
            task.status = Status.COMPLETED
            task.save(update_fields=["status"])
            messages.success(request,"כל הכבוד! הססטוס עודכן!")
            return redirect("home")
        else:
            messages.error(request,"אין אפשרות לשנות סטטוס משימה שכבר משויכת לעובד אחר")
    return redirect("home")


def about(request):
    return render(request, "about.html")