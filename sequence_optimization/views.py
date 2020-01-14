from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic

from sequence_optimization.forms import AddSequenceForm
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


class RegisterUser(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'sequence_optimization/registration.html'


class AddSequence(generic.CreateView):
    form_class = AddSequenceForm
    success_url = reverse_lazy('')
    template_name = 'sequence_optimization/add_sequence.html'
