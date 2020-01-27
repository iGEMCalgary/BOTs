import random
from Bio.SeqUtils import seq3
from sequence_optimization.spea2_optimization_suite.fitness import *


def get_parents(archive):
    selected = sorted(archive, key=get_sum_fitness, reverse=False)
    return selected[:math.ceil(0.2 * len(archive))]


def get_density(elem):
    return getattr(elem, "density")


def populate_archive_with_remaining_best(archive, archive_size, dominated):
    num_individuals_to_add = archive_size - len(archive)
    dominated_set = sorted(dominated, key=lambda sequence:
    getattr(sequence, "gc_fitness") +
    getattr(sequence, "homo_fitness") +
    getattr(sequence, "host_fitness") +
    getattr(sequence, "repeats_fitness") +
    getattr(sequence, "restriction_fitness") +
    getattr(sequence, "splice_fitness") +
    getattr(sequence, "start_fitness") +
    getattr(sequence, "hairpins_fitness"), reverse=False)
    dominated_set = dominated_set[:num_individuals_to_add]
    archive.extend(dominated_set)
    return archive


def calculate_fitness(population, gc_parameters, ancestor_sequence, restriction_sites):
    for individual in population:
        assert isinstance(individual, SequenceContainer)
        setattr(individual, "gc_fitness", eval_gc_content(individual, gc_parameters))
        setattr(individual, "homo_fitness", eval_homopolymers(individual))
        setattr(individual, "host_fitness", eval_host(individual, ancestor_sequence))
        setattr(individual, "repeats_fitness", eval_repeats(individual))
        setattr(individual, "restriction_fitness", eval_restriction_sites(individual, restriction_sites))
        setattr(individual, "splice_fitness", eval_splice_sites(individual))
        setattr(individual, "start_fitness", eval_start_sites(individual))
        setattr(individual, "hairpins_fitness", eval_hairpins(individual))


def initialize_population(population_size, problem_size, ancestor_sequence, probability_mutation, codon_use_table):
    """
    Initializes a population of sequences based on a (hopefully) codon optimized
    sequence
    :param codon_use_table:
    :param probability_mutation: float determines probability of mutation
    :param population_size: int determines minimum population size
    :param problem_size: int helps determines minimum population size
    :param ancestor_sequence: Bio.seq.seq codon optimized sequence
    :return:
    """
    population = []
    mutable_seq = ancestor_sequence.tomutable()
    if problem_size < population_size:
        size = population_size
    else:
        size = problem_size
    for idx in range(size):
        population.append(SequenceContainer(mutable_seq.toseq()))
        mutate_sequence(population[-1], codon_use_table, probability_mutation)

    return population


def mutate_sequence(individual, codon_use_table, mutation_probability=0.05, offset=0):
    """
    Takes a single sequence and gives it a random number of mutations.
    :param individual:
    :param codon_use_table:
    :param mutation_probability:
    :param offset:
    :return:
    """
    assert isinstance(individual, SequenceContainer)
    sequence = getattr(individual, "sequence")
    mutable_seq = sequence.tomutable()
    num_codons = len(mutable_seq) // 3
    num_mutations = math.ceil(num_codons * mutation_probability)
    for _ in range(num_mutations):
        position = 3 * random.randrange(0, len(mutable_seq) // 3)
        codon_idx = slice(offset + position, (offset + 3) + position)
        new_codon = mutate_codon(mutable_seq[codon_idx], codon_use_table)
        mutable_seq[codon_idx] = new_codon
    return mutable_seq.toseq()


def mutate_codon(codon_in, codon_use_table):
    """Select a synonymous codon in accordance with the frequency of use
    in the host organism.
    Args:
    codon_in (Bio.Seq.Seq): A single codon.
    Returns:
        Bio.Seq.Seq: A new codon.
    """
    amino_acid = seq3(CodonTable.standard_dna_table.forward_table[str(codon_in)]).upper()
    synonymous_codons, codon_use_freq = codon_use_table[amino_acid]
    if len(synonymous_codons) == 1:
        return codon_in

    # pick new codon
    codon_out = codon_in
    while codon_in == codon_out:
        codon_out = random.choices(synonymous_codons, codon_use_freq).pop()

    return codon_out


def optimize_with_strength_pareto_evolutionary_algorithm(population_size, archive_size, problem_size,
                                                         probability_crossover, probability_mutation,
                                                         ancestor_sequence, codon_use_table, gc_parameters,
                                                         restriction_sites):
    population = initialize_population(population_size, problem_size, ancestor_sequence, probability_mutation,
                                       codon_use_table)
    archive = []
    for generation in range(0, max_generations):
        calculate_fitness(population, gc_parameters, ancestor_sequence, restriction_sites)
        union = population.copy()
        union.extend(archive)
        nearest_neighbours = determine_neighbours(union)
        calculate_solution_density(union, nearest_neighbours)
        for individual in union:
            calculate_raw_fitness(individual)
        archive, dominated = get_non_dominated_solutions(union)
        if len(archive) < archive_size:
            archive = populate_archive_with_remaining_best(archive, archive_size, dominated)
        elif len(archive) > archive_size:
            archive = truncate_similar_individuals(archive, archive_size)
        parents = get_parents(archive)
        population = crossover_and_mutate(parents, probability_crossover, probability_mutation, codon_use_table)

    for item in archive:
        print(getattr(item, "sequence"))
    return archive
