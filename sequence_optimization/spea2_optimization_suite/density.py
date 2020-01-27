def determine_neighbours(union):
    neighbours = [[0 for x in range(len(union))] for y in range(len(union))]
    for idx in range(len(union)):
        for jdx in range(len(union)):
            if idx != jdx:
                distance = n_dimensional_euclidian_distance(union[idx], union[jdx])
                neighbours[idx][jdx] = neighbours[jdx][idx] = distance
    return neighbours

def calculate_solution_density(union, nearest_neighbours):
    """
    Evaluate distance between kth nearest neighbours, where k is sqrt(len(union))
    :param nearest_neighbours:
    :param union:
    :return:
    """
    kth = math.ceil(math.sqrt(len(union)))
    for idx in range(len(union)):
        assert isinstance(union[idx], SequenceContainer)
        setattr(union[idx], "density", sorted(nearest_neighbours[idx])[kth])

def get_non_dominated_solutions(union):
    """
    Determine pareto dominance, that is
    dominant: solution that has the best scores without betraying the other scores
    non-dominant: solution that betrays the scores, compared to another one
    its a two way relationship
    :param union:
    :return:
    """
    non_dominated_set = []
    dominated_set = []
    pareto_dominance_graph = [[True for x in range(len(union))] for y in range(len(union))]
    # if any vector is larger it is dominated, else it is not dominated
    for idx in range(len(union)):
        for jdx in range(len(union)):
            if getattr(union[idx], "gc_fitness") > getattr(union[jdx], "gc_fitness") or \
                    getattr(union[idx], "homo_fitness") > getattr(union[jdx], "homo_fitness") or \
                    getattr(union[idx], "host_fitness") > getattr(union[jdx], "host_fitness") or \
                    getattr(union[idx], "repeats_fitness") > getattr(union[jdx], "repeats_fitness") or \
                    getattr(union[idx], "restriction_fitness") > getattr(union[jdx], "restriction_fitness") or \
                    getattr(union[idx], "splice_fitness") > getattr(union[jdx], "splice_fitness") or \
                    getattr(union[idx], "start_fitness") > getattr(union[jdx], "start_fitness") or \
                    getattr(union[idx], "hairpins_fitness") > getattr(union[jdx], "hairpins_fitness"):
                pareto_dominance_graph[idx][jdx] = False
    for idx in range(len(union)):
        add = True
        for jdx in range(len(union)):
            if pareto_dominance_graph[idx][jdx] is False:
                add = False
                break
        if add is True:
            non_dominated_set.append(union[idx])
        else:
            dominated_set.append(union[idx])
    return non_dominated_set, dominated_set


def truncate_similar_individuals(archive, archive_size):
    sorted_archive = sorted(archive, key=get_density, reverse=False)
    return sorted_archive[archive_size:]

def n_dimensional_euclidian_distance(individual1, individual2):
    assert isinstance(individual2, SequenceContainer) and isinstance(individual1, SequenceContainer)
    gc = (getattr(individual2, "gc_fitness") - getattr(individual1, "gc_fitness")) ** 2
    homo = (getattr(individual2, "homo_fitness") - getattr(individual1, "homo_fitness")) ** 2
    host = (getattr(individual2, "host_fitness") - getattr(individual1, "host_fitness")) ** 2
    repeat = (getattr(individual2, "repeats_fitness") - getattr(individual1, "repeats_fitness")) ** 2
    restriction = (getattr(individual2, "restriction_fitness") - getattr(individual1, "restriction_fitness")) ** 2
    splice = (getattr(individual2, "splice_fitness") - getattr(individual1, "splice_fitness")) ** 2
    start = (getattr(individual2, "start_fitness") - getattr(individual1, "start_fitness")) ** 2
    hairpin = (getattr(individual2, "hairpins_fitness") - getattr(individual1, "hairpins_fitness")) ** 2
    return math.sqrt(gc + homo + host + repeat + restriction + splice + start + hairpin)



def calculate_raw_fitness(individual):
    """
    Determine the fitness relative to the others based on how dominant they are
    :param individual:
    :return:
    """
    pass