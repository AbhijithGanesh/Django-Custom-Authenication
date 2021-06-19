from django.contrib import admin
from .models import *

myModels = [Employee, Project, ProjectTask]
admin.site.register(myModels)
