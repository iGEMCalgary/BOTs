from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from sequence_optimization.models import *


def index(request):
    ancestor_sequence_list = AncestorSequence.objects.order_by('sequence')
    template = loader.get_template('sequence_optimization/index.html')
    context = {
        'ancestor_sequence_list': ancestor_sequence_list,
    }
    return HttpResponse(template.render(context, request))
