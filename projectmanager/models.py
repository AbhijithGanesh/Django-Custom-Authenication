from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser

def EmployeeIDGenerator():
    import random
    output = ""
    for i in range(2):
        output += str(random.choice([chr(j) for j in range(65,91)])) + str(random.choice(list(range(1,10)))) + str(random.choice([chr(k) for k in range(97,123)]))
    return output

class Employee(models.Model):
    Name = models.CharField(max_length = 200, unique = False, primary_key = True)
    EmployeeID = models.CharField(max_length = 100, default = EmployeeIDGenerator, unique = True)
    EMail = models.EmailField(max_length=254, unique = True)
    Contact = models.IntegerField()
    Manager_Status = models.BooleanField(default = False)

class Project(models.Model):
    Time_and_Date_Created = models.DateField(auto_now_add = True)
    Project_Title = models.CharField(max_length = 100)
    Project_Description = models.TextField()
    Project_Manager = models.ForeignKey(Employee, on_delete = models.CASCADE,null = False)
    Project_Link = models.URLField(max_length = 200, unique = True, null = False)
    Project_Gravatar = models.URLField(max_length = 200, unique = False)

class ProjectTask(models.Model):
    Task_Reference = models.ForeignKey(Project, on_delete = models.CASCADE)
    Time_Created = models.TimeField(auto_now_add = True)
    Task = models.TextField()
    Subtasks = models.TextField()


