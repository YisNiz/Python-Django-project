from django.db import models
from django.contrib.auth.models import AbstractUser


#   Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=255)
    admin = models.OneToOneField('CustomUser', on_delete=models.CASCADE,related_name='team_admin',null=True,blank=True)

    def __str__(self):
        return self.name

class Role(models.TextChoices):
    ADMIN='admin',"Admin"
    USER='user',"User"

class CustomUser(AbstractUser):
    role = models.CharField(choices=Role.choices, max_length=255,default=Role.USER)
    team = models.ForeignKey('Team',null=True,blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return self.role+" "+self.username

class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    worker=models.ForeignKey('CustomUser',blank=True,null=True,on_delete=models.SET_NULL)
    team=models.ForeignKey('Team',on_delete=models.CASCADE)
    created_by=models.ForeignKey('CustomUser',on_delete=models.CASCADE,related_name='created_tasks')
    finishDate = models.DateField()
    status = models.CharField(choices=Status.choices,max_length=255,default=Status.NEW)

    def __str__(self):
        return self.name+" "+self.worker.username if self.worker else self.name+" no worker allredy"
