from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from sequence_optimization.models import *


def index(request):
    if request.user.is_authenticated:
        # show all sequences owned by user
        ancestor_sequence_list = AncestorSequence.objects.order_by('sequence')
        context = {
            'ancestor_sequence_list': ancestor_sequence_list,
            'login_status': True,
        }
        template = loader.get_template('sequence_optimization/index.html')
        return HttpResponse(template.render(context, request))
    else:
        # blank
        template = loader.get_template('sequence_optimization/index.html')
        context = {'login_status': False, }
        return HttpResponse(template.render(context, request))


def login_user(request):
    template = loader.get_template('sequence_optimization/user.html')
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
    return HttpResponse(template.render(context, request))


def add_sequence(request):
    template = loader.get_template('sequence_optimization/add_sequence.html')
    context = {}
    return HttpResponse(template.render(context, request))
