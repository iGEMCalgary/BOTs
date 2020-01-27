import re

from django import forms
from django.core.exceptions import ValidationError

from sequence_optimization.models import *


class OptimizeSequenceForm(forms.Form):
    sequence_parameters = forms.ModelChoiceField(queryset=SequenceParameters.objects.all(), required=False)

    def __init__(self, username):
        super().__init__()


class AddSequenceForm(forms.Form):
    sequence = forms.CharField(label='Sequence 50+', max_length=100000, min_length=50, required=True)
    host = forms.CharField(label='Host', max_length=10, min_length=2, required=True)

    population_size = forms.IntegerField(label='Population Size 5-1000', max_value=1000, min_value=5, required=True)
    archive_size = forms.IntegerField(label='Archive Size 5-1000', max_value=1000, min_value=5, required=True)
    minimum_codon_occurence = forms.DecimalField(label='Minimum Codon Occurence 0-1', min_value=0, max_value=1,
                                                 required=True)
    mutation_probability = forms.DecimalField(label='Mutation Probability 0-1', max_value=1, min_value=0, required=True)
    crossover_probability = forms.DecimalField(label='Mutation Probability 0-1', max_value=1, min_value=0,
                                               required=True)
    max_generations = forms.IntegerField(label='Max Number of Generations 5-500', min_value=5, max_value=500,
                                         required=True)

    restriction_enzymes = forms.CharField(label='Restriction Enzymes', max_length=100, required=False)
    gc = forms.ModelMultipleChoiceField(label='Choose GC Parameters', queryset=GCInfo.objects.all(), required=False)

    # all different optimizations
    minimize_splice_sites = forms.BooleanField(label='Minimize Splice Sites', required=False)
    minimize_alternate_start_sites = forms.BooleanField(label='Minimize Alternate Start Sites', required=False)
    minimize_hairpins = forms.BooleanField(label='Minimize Hairpins', required=False)
    minimize_homopolymers = forms.BooleanField(label='Minimize Homopolymers', required=False)
    minimize_repeats = forms.BooleanField(label='Minimize Repeats', required=False)
    optimize_codons = forms.BooleanField(label='Optimize Codons', required=False)

    table_path = forms.FileField(label='Custom Host File', required=False)

    def clean(self):
        cd = self.cleaned_data  # dict
        # clean whitespace
        cd['sequence'] = str("".join(str(cd.get("sequence")).split())).replace('\\n', '')
        if re.search("[^ACDEFGHILKMNPQRSTVWY]",  cd['sequence']) is not None:
            raise ValidationError("Sequence is not Amino Acids")
        # if host not on kasuza
        # if restriction enzymes dont exist
        # if table file is wrong
        return cd
