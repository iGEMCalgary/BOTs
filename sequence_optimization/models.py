# Create your models here.
from Bio import Seq
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class AncestorSequence(models.Model):
    sequence = models.CharField(max_length=100000, blank=False, primary_key=True)

    def __str__(self):
        return 'Base Sequence: %s' % self.sequence


class AncestorSequenceOptimized(models.Model):
    ancestor_sequence = models.ForeignKey(AncestorSequence, on_delete=models.PROTECT, null=False, blank=False)
    host = models.CharField(max_length=10, blank=False, null=False)
    optimized_sequence = models.CharField(max_length=100000, blank=False, null=False)

    class Meta:
        unique_together = [['ancestor_sequence', 'host']]

    def __str__(self):
        return str(self.ancestor_sequence) + \
               '\n host: %s\n optimized_sequence: %s' % (self.host, self.optimized_sequence)


class SequenceParameters(models.Model):
    """
    Stores arguments supplied for the sequence
    arguments are supplied as dict (unpack json in argument)
    """
    # Key
    sequence = models.ForeignKey(AncestorSequenceOptimized, on_delete=models.PROTECT, null=False, blank=False)
    date_mutated = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, blank=False)  # auto gen

    # Never null
    population_size = models.PositiveSmallIntegerField(blank=False, null=False, validators=[
        MinValueValidator(5, "Population must be greater or equal to 5"),
        MaxValueValidator(1000, "Population must be smaller than 1000")])
    archive_size = models.PositiveSmallIntegerField(blank=False, null=False, validators=[
        MinValueValidator(5, "Archive must be greater or equal to 5"),
        MaxValueValidator(1000, "Archive must be smaller or equal to 1000")])

    minimum_codon_occurence = models.DecimalField(blank=False, null=False, validators=[
        MinValueValidator(0, "Minimum codon occurence must be greater or equal to 0"),
        MaxValueValidator(1, "Minimum codon occurence must be smaller or equal to 1")])

    mutation_probability = models.DecimalField(max_digits=4, decimal_places=3, blank=False, null=False, validators=[
        MaxValueValidator(1, "Mutation probability must be between 0 and 1"),
        MinValueValidator(0, "Mutation probability must be between 0 and 1")])
    crossover_probability = models.DecimalField(max_digits=4, decimal_places=3, blank=False, null=False, validators=[
        MaxValueValidator(1, "Mutation probability must be between 0 and 1"),
        MinValueValidator(0, "Mutation probability must be between 0 and 1")])

    restriction_enzymes = models.CharField(max_length=100, blank=False, null=False)
    remove_splice_sites = models.BooleanField(blank=False, null=False)
    remove_alternate_start_sites = models.BooleanField(blank=False, null=False)

    max_generations = models.PositiveSmallIntegerField(blank=False, null=False, validators=[
        MinValueValidator(5, "Generations must be greater or equal to 5"),
        MaxValueValidator(500, "Generations must be smaller or equal to 500")])

    # Can be null
    # associated user
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    # TODO: Revisit table path
    # TODO: Add the new bool fields
    table_path = models.FilePathField(default=None, blank=True, null=True)
    gc = models.ManyToManyField('GCInfo', through='GCParameters')

    class Meta:
        unique_together = [['sequence', 'date_mutated']]

    def __str__(self):
        return str(self.sequence) + \
               '\n population size: %s ' \
               '\n archive size: %s ' \
               '\n minimum codon occurence: %s ' \
               '\n mutation probability: %s ' \
               '\n crossover probability: %s ' \
               '\n removes splice sites: %s ' \
               '\n removes alternate start sites: %s ' \
               '\n max generations: %s' % \
               (self.population_size,
                self.archive_size,
                self.minimum_codon_occurence,
                self.mutation_probability,
                self.crossover_probability,
                self.remove_splice_sites,
                self.remove_alternate_start_sites,
                self.max_generations)


class MutatedSequence(models.Model):
    # key
    parameters = models.ForeignKey(SequenceParameters, on_delete=models.PROTECT, blank=False, null=False)
    mutated_sequence = models.CharField(max_length=100000, blank=False, null=False)

    # fitness
    hairpin_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                          validators=[MinValueValidator(0, "Fitness must be positive")])
    alternate_start_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                                  validators=[MinValueValidator(0, "Fitness must be positive")])
    gc_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                     validators=[MinValueValidator(0, "Fitness must be positive")])
    homopolymer_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                              validators=[MinValueValidator(0, "Fitness must be positive")])
    codon_optimization_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True,
                                                     default=None,
                                                     validators=[MinValueValidator(0, "Fitness must be positive")])
    repeats_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                          validators=[MinValueValidator(0, "Fitness must be positive")])
    restriction_enzyme_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True,
                                                     default=None,
                                                     validators=[MinValueValidator(0, "Fitness must be positive")])
    splice_site_fitness = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True, default=None,
                                              validators=[MinValueValidator(0, "Fitness must be positive")])

    # non-fitness
    generation = models.PositiveSmallIntegerField(blank=False, null=False, validators=[
        MinValueValidator(0, "Minimum codon occurence must be greater or equal to 0")])

    class Meta:
        unique_together = ['parameters', 'mutated_sequence']

    def __str__(self):
        return str(self.parameters) + \
               '\n mutated_sequence: %s' \
               '\n Fitness:' \
               '\n hairpin: %s' \
               '\n alternate start: %s' \
               '\n gc: %s' \
               '\n homopolymer: %s' \
               '\n codon optimization: %s' \
               '\n repeats: %s' \
               '\n restriction enzymes: %s' \
               '\n splice site: %s' % (
                   self.mutated_sequence,
                   self.hairpin_fitness,
                   self.alternate_start_fitness,
                   self.gc_fitness,
                   self.homopolymer_fitness,
                   self.codon_optimization_fitness,
                   self.repeats_fitness,
                   self.restriction_enzyme_fitness,
                   self.splice_site_fitness
               )


class GCInfo(models.Model):
    name = models.CharField(max_length=25, blank=False, primary_key=True)
    minimum_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False,
                                             validators=[MinValueValidator(0, "Minimum must be positive")])
    maximum_percentage = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    frame_size = models.PositiveSmallIntegerField(blank=False, null=False)
    parameters = models.ManyToManyField(SequenceParameters, through='GCParameters')

    def __str__(self):
        return '%s\n min: %s\n max: %s\n frame: %s' % (
            self.name, self.minimum_percentage, self.maximum_percentage, self.frame_size)


class GCParameters(models.Model):
    info = models.ForeignKey(GCInfo, on_delete=models.PROTECT, blank=False, null=False)
    parameter = models.ForeignKey(SequenceParameters, on_delete=models.PROTECT, blank=False, null=False)

    class Meta:
        unique_together = [['info', 'parameter']]
