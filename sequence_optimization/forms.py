from django import forms

from sequence_optimization.models import GCInfo


class AddSequenceForm(forms.Form):
    sequence = forms.CharField(label='Sequence', max_length=100000, min_length=50, required=True)
    host = forms.CharField(lebel='Host', max_length=10, min_length=2, required=True)

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
    optimizations = forms.MultipleChoiceField(label='Other optimizations',
                                              choices=(
                                                  'Minimize Splice Sites',
                                                  'Minimize Alternate Start Sites',
                                                  'Minimize Hairpins',
                                                  'Minimize Homopolymers',
                                                  'Minimize Repeats',
                                                  'Optimize Codons',
                                              ))

    table_path = forms.FilePathField(label='Custom Host Path')
