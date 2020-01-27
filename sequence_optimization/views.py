from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic

from sequence_optimization.forms import AddSequenceForm, OptimizeSequenceForm
from sequence_optimization.models import *


def index(request):
    if request.user.is_authenticated:
        # show all sequences owned by user
        ancestor_sequence_list = AncestorSequence.objects.order_by('sequence')
        context = {
            'ancestor_sequence_list': ancestor_sequence_list,
        }
        template = loader.get_template('sequence_optimization/index.html')
        return HttpResponse(template.render(context, request))
    else:
        # blank
        template = loader.get_template('sequence_optimization/index.html')
        context = {}
        return HttpResponse(template.render(context, request))


class RegisterUser(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'sequence_optimization/registration.html'


def add_sequence(request):
    if request.method == 'GET':  # initial visit
        form = AddSequenceForm()
        context = {
            'form': form
        }
        template = loader.get_template('sequence_optimization/add_sequence.html')
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':  # form submitted
        form = AddSequenceForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.cleaned_data
            context = {
                'form': form
            }
            template = loader.get_template('sequence_optimization/index.html')
            return HttpResponse(template.render(context, request))
        else:
            raise Http404("Invalid Form")


def optimize_sequence(request):
    if request.method == 'GET':
        form = OptimizeSequenceForm()
        context = {
            'form': form
        }
        template = loader.get_template('sequence_optimization/optimize_sequence.html')
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        form = OptimizeSequenceForm(request.BODY, request.FILES)
        if form.is_valid():
            form = form.cleaned_data
            context = {
                'form': form,
            }
            SPEA2_optimizer(form)
            template = loader.get_template('sequence_optimization/index.html')
            return HttpResponse(template.render(context, request))
        else:
            raise Http404("Invalid Form")
