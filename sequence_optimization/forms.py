import re

from django import forms

from sequence_optimization.models import GCInfo


class AddSequenceForm(forms.Form):
    sequence = forms.CharField(label='Sequence', max_length=100000, min_length=50, required=True)
    host = forms.CharField(label='Host', max_length=10, min_length=2, required=True)

    population_size = forms.IntegerField(label='Population Size', max_value=1000, min_value=5, required=True)
    archive_size = forms.IntegerField(label='Archive Size', max_value=1000, min_value=5, required=True)
    minimum_codon_occurence = forms.DecimalField(label='Minimum Codon Occurence', min_value=0, max_value=1,
                                                 required=True)
    mutation_probability = forms.DecimalField(label='Mutation Probability', max_value=1, min_value=0, required=True)
    crossover_probability = forms.DecimalField(label='Mutation Probability', max_value=1, min_value=0, required=True)
    max_generations = forms.IntegerField(label='Max Number of Generations', min_value=5, max_value=500, required=True)

    restriction_enzymes = forms.CharField(label='Restriction Enzymes', max_length=100)
    gc = forms.ModelMultipleChoiceField(queryset=GCInfo.objects.all())
    # all different optimizations

    minimize_splice_sites = forms.BooleanField(label='Minimize Splice Sites')
    minimize_alternate_start_sites = forms.BooleanField(label='Minimize Alternate Start Sites')
    minimize_hairpins = forms.BooleanField(label='Minimize Hairpins')
    minimize_homopolymers = forms.BooleanField(label='Minimize Homopolymers')
    minimize_repeats = forms.BooleanField(label='Minimize Repeats')
    optimize_codons = forms.BooleanField(label='Optimize Codons')

    table_path = forms.FileField(label='Custom Host File')

    def is_valid(self):
        valid = super(AddSequenceForm, self).is_valid()
        if not valid:
            return False
        if re.search("^[ACDEFGHILKMNPQRSTVWY]", str(self.sequence)) is not None:
            return False
        # if host not on kasuza
        # if restriction enzymes dont exist
        # if table file is wrong
