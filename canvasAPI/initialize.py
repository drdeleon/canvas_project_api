from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, remove_perm

from assistants.models import Assistant

professors = Group.objects.create(name='professors')
students = Group.objects.create(name='students')
assistants = Group.objects.create(name='assistants')